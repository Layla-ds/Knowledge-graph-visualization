from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.shortcuts import reverse
import json as JSON
import time

from py2neo import Graph
graph = Graph("http://localhost:7474", auth=("yourUserName", "yourPassWord"))


def index(request):
    return render(request, 'kg/index.html')


def get_initial_graph(request):    #home
    kword ='China'
    # kword = 'China'
    split_keys = kword.split(',')
    for key in split_keys:
        element = get_node_edges_1(key)
    elements = {"elements": element}
    return JsonResponse(elements)


def search(request):
    if request.method == 'GET':
        kword = request.session.get('name_title')
        return render(request, 'kg/index.html', context={"entity": kword})
    else:
        request.session['name_title'] = request.POST.get('name_title')
        return redirect(reverse('search'))
    # return render(request, 'search.html', context={"entity": kword})


def get_graph(request, entity):   #search
    kword = entity
    if kword.count(',') == 0:
        element = get_node_edges_1(kword)
    elif kword.count(',') == 1:
        element = get_node_edges_2(kword)
    else:
        element = get_node_edges_3(kword)
    elements = {"elements": element}
    return JsonResponse(elements)

def get_node_edges_1(kword):
    if kword:
        c1 = 'MATCH (a)-[r]->(n) WHERE a.entityName=\'' + kword + '\' RETURN a,n,r,labels(n),n.entityImportance'
        start = time.time()
        ### time start
        s1 = graph.run(c1).data()# one hop
        selected = select_node_edges(s1, 50)
        nodes = list(map(buildSelf, selected)) + list(map(buildNodes, selected))
        edges = list(map(buildEdges, selected))
        elements = {"nodes": nodes, "edges": edges}
        ### time end
        mid = time.time()
        print(mid - start) ### print time
    return elements  #这里可以直接return nodes和edges,在get_initial graph 里调用


def get_node_edges_2(kword):
    kword1 = kword.split(',')[0]
    kword2 = kword.split(',')[1]
    c1 = 'MATCH p=allShortestPaths((n1{entityName:\''+kword1+'\'})-[*]->(n2{entityName:\''+kword2+'\'})) return p'
    start = time.time()
    ### time start
    s1 = graph.run(c1).data()
    nodes = []
    edges = []
    for i in range(len(s1)):
        nodes = nodes + list(map(buildNodes2, s1[i]['p'].nodes))
        edges = edges + list(map(buildEdges2, s1[i]['p'].relationships))
    elements = {"nodes": nodes, "edges": edges}
    ### time end
    mid = time.time()
    print(mid - start)
    return elements


def get_node_edges_3(kword):
    if kword:
        split_keys = kword.split(',')
        nodes = []
        edges = []
        for key in split_keys:
            c1 = 'MATCH (a)-[r]->(n) where a.entityName =~ \'' + key + '\' RETURN a,n,r,n.entityImportance,labels(n) limit 10'
            c2 = 'MATCH (a)-[r2]->(b)-[r]->(n) where a.entityName =~ \'' + key + '\' RETURN r,n,n.entityImportance,labels(n) limit 30'
            start = time.time()
            ### time start
            s1 = graph.run(c1).data()# one hop
            s2 = graph.run(c2).data()# two hop
            nodes = nodes + (list(map(buildSelf, s1)) + list(map(buildNodes, s1)) + list(map(buildNodes, s2)))
            edges = edges + (list(map(buildEdges, s1)) + list(map(buildEdges, s2)))
        elements = {"nodes": nodes, "edges": edges}
        ### time end
        mid = time.time()
        print(mid - start) ### print time
    return elements


def buildSelf(nodeRecord):
    data = {"id": nodeRecord['a'].identity, "label": list(nodeRecord['a'].labels)[0],
            "name": nodeRecord['a']['entityName'], "entityId": nodeRecord['a']['entityId'],
            "entityImportance": nodeRecord['a']['entityImportance'],
            "entityProperty": nodeRecord['a']['entityProperty']}
    return {"data": data}


def buildNodes(nodeRecord):
    data = {"id": nodeRecord['n'].identity, "label": list(nodeRecord['n'].labels)[0],
            "name": nodeRecord['n']['entityName'], "entityId": nodeRecord['n']['entityId'],
            "entityImportance": nodeRecord['n']['entityImportance'],
            "entityProperty": nodeRecord['n']['entityProperty']}
    return {"data": data}


def buildEdges(relationRecord):
    data = {"id": relationRecord['r'].identity,
            "source": relationRecord['r'].start_node.identity,
            "target": relationRecord['r'].end_node.identity,
            "relationship": list(relationRecord['r'].types())[0],
            "direction": relationRecord['r']['inverse']}
    return {"data": data}


def buildNodes2(nodeRecord):
    data = {"id": nodeRecord.identity, "label": list(nodeRecord.labels)[0],
            "name": nodeRecord['entityName'], "entityId": nodeRecord['entityId'],
            "entityImportance": nodeRecord['entityImportance'],
            "entityProperty": nodeRecord['entityProperty']}
    return {"data": data}


def buildEdges2(relationRecord):
    data = {"id": relationRecord.identity,
            "source": relationRecord.start_node.identity,
            "target": relationRecord.end_node.identity,
            "relationship": list(relationRecord.types())[0],
            "direction": relationRecord['inverse']}
    return {"data": data}


def select_node_edges(s1, k):
    # extract all data in lists
    a = []
    n = []
    r = []
    importance = []
    label = []
    for i in range(len(s1)):
        a.append(s1[i]['a'])
        n.append(s1[i]['n'])
        r.append(s1[i]['r'])
        importance.append(float(s1[i]['n.entityImportance']))
        label.append(s1[i]['labels(n)'][0])
    # select nodes and edges
    entity_temp = n
    relationship_temp = r
    coverage = [1 for i in range(len(importance))]
    selected_entity = list()
    selected_relationship = list()
    # if number of entities is bigger than limit number of entities
    if len(importance) >= k:
        count = 0
        lamb = 0.6
        while count < k:
            values = list()
            # calculate value of all entity and select the biggest one
            for i in range(len(importance)):
                v = lamb * importance[i] + (1 - lamb) * coverage[i]
                values.append(v)
            max_index = values.index(max(values))
            # add selected entity into list 'selected'
            selected_entity.append(entity_temp[max_index])
            selected_relationship.append(relationship_temp[max_index])
            # store label name as a variable
            label_name = label[max_index]
            # delete selected entity from four lists
            del entity_temp[max_index]
            del relationship_temp[max_index]
            del importance[max_index]
            del label[max_index]
            del coverage[max_index]
            # change coverage of entity with selected label to 0
            for i in range(len(coverage)):
                if label[i] == label_name:
                    coverage[i] = 0
            count += 1
    else:
        selected_entity = entity_temp
        selected_relationship = relationship_temp
    # integral as a new graph list
    selected = []
    for i in range(len(selected_entity)):
        dic = dict()
        dic['a'] = a[i]
        dic['n'] = selected_entity[i]
        dic['r'] = selected_relationship[i]
        selected.append(dic)
    return selected


def add_node(request):
    # return render(request, 'hello.html')
    return render(request, 'kg/add-node.html');


def add_node_api(request):
    # return render(request, 'hello.html')
    json_str = request.body
    if not json_str:
        result = {'code': 202, 'error': 'Please POST data!!'}
        return JsonResponse(result)
    # 如果当前报错,请执行 json_str = json_str.decode()
    backdata = {'status': 0, 'data': ''}
    json = JSON.loads(json_str)
    try:
        result = graph.run(json.get("command")).data()
        backdata = {'status': 1, 'data': result}
    except Exception as ex:
        result = ex
        backdata['status'] = 2
        backdata['data'] = str(ex)
    return JsonResponse(backdata)