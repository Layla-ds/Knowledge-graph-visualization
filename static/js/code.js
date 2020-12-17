$(function () {
    $.get('graph', function (result) {
        var graph = window.cy = cytoscape({
            container: document.getElementById('graph'),
            style: cytoscape.stylesheet()
                .selector('node[label = "Organisation"]').css({'background-color': '#60418F', "text-outline-color":'#60418F', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2}) //节点样式
                .selector('node[label = "Person"]').css({'background-color': '#EE2C34', "text-outline-color":'#EE2C34', 'content': 'data(name)', "text-valign" : "center", //节点样式
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})
                .selector('node[label = "Award"]').css({'background-color': '#DCAFD0', "text-outline-color":'#DCAFD0', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Device"]').css({'background-color': '#A18055', "text-outline-color":'#A18055', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Event"]').css({'background-color': '#EF8E19', "text-outline-color":'#EF8E19', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Food"]').css({'background-color': '#FFD700', "text-outline-color":'#FFD700', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Transportation"]').css({'background-color': '#5F2E20', "text-outline-color":'#5F2E20', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Place"]').css({'background-color': '#43C565', "text-outline-color":'#43C565', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Species"]').css({'background-color': '#179587', "text-outline-color":'#179587', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "TimePeriod"]').css({'background-color': '#7697DE', "text-outline-color":'#7697DE', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Work"]').css({'background-color': '#B362A5', "text-outline-color":'#B362A5', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Thing"]').css({'background-color': '#58C1DA', "text-outline-color":'#58C1DA', 'content': 'data(name)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})//节点样式
                .selector('node[label = "Activity"]').css({'background-color': '#E69A8D', "text-outline-color":'#E69A8D', 'content': 'data(title)', "text-valign" : "center",
                    'width': 80, 'height': 80, 'font-size':18,'color': 'white',"text-wrap": "wrap", "text-max-width": 10,'text-outline-width': 2})
                .selector('edge').css({
                    'font-size':14,
                    'curve-style': 'bezier',
                    //'target-arrow-shape': 'circle',
                    'line-color': '#adadad',
                    'target-arrow-color': '#adadad',
                    'content': 'data(relationship)',
                    'width': 2,
                    'edge-text-rotation': 'autorotate'

                }) //边线样式
                .selector(':selected').css({
                    'background-color': '#000000',
                    'line-color': '#000000',
                    'target-arrow-color': '#000000',
                    'source-arrow-color': '#000000',
                    "text-outline-color":'#000000',
                    'opacity': 1

                }) //点击后节点与边的样式
                .selector('.faded').css({'opacity': 0.25, 'text-opacity': 0}),
            layout: {name: 'cose', fit: true},
            // layout: {name: 'cose', fit: true},  二条速度极慢，会崩
            elements: result.elements,
            zoom: 1,//图的初始缩放级别。
            pan: { x: 0, y: 0 },//图的初始平移位置。
            minZoom: 1e-50, // 图表缩放级别的最小界限.视口的缩放比例不能小于此缩放级别.
            maxZoom: 1e50, // 图表缩放级别的最大界限.视口的缩放比例不能大于此缩放级别.

        });
        // var highlightNextEle = function(){
        //     if( i < bfs.path.length ){
        //          bfs.path[i].addClass('highlighted');
        //          i++;
        //         setTimeout(highlightNextEle, 1000);
        //      }
        // var bfs = graph.elements().bfs('#a', function(){}, true);
        graph.nodes().forEach(function (n) {
            debugger
            n.on('click', function (e) {
                let json = e.target.data()
                console.log(json)
                $("#jsonview").JSONView(json);
                document.getElementById("jsonview").innerHTML = document.getElementById("jsonview").innerHTML.replace(/{/, "").replace(/}/, "")
                // with options
                // $("#json-collasped").JSONView(json, {collapsed: true});
            });
        })
        graph.edges().forEach(function (n) {
            debugger
            n.on('click', function (e) {
                let json = e.target.data()
                console.log(json)
                $("#jsonview").JSONView(json);
                document.getElementById("jsonview").innerHTML = document.getElementById("jsonview").innerHTML.replace(/{/, "").replace(/}/, "")
                // with options
                // $("#json-collasped").JSONView(json, {collapsed: true});
            });
        })
    }, 'json');
})
;