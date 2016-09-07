var nodeIds, shadowState, nodesArray, nodes, edgesArray, edges, network;

var activatedColor = {
                        background: '#66ff66',
                        border: '#00b300',
                        highlight: {
                                background: '#b3ffb3',
                                border: '#00ff00'
                            }
                        };
var sensorColor = {
                        background: '#ff9900',
                        border: '#b36b00',
                        highlight: {
                            background: '#ffc266',
                            border: '#b36b00'
                        }
                    }

    function startNetwork() {
        // this list is kept to remove a random node.. we do not add node 1 here because it's used for changes
        shadowState = false;
        currentNodeId = -1;


        // create an array with nodes and sensors
        nodesBaseArray = [
            {id: '1', label: 'Elsa', group: 'nodes'},
            {id: '2', label: 'Belle', group: 'sensors'},
            {id: '3', label: 'Aurora', group: 'sensors'}
        ];
        nodes = new vis.DataSet(nodesBaseArray);

        // create an array with edges
        edgesArray = [
            {id: '1', from: '1', to: '2' },
            {id: '2', from: '2', to: '3' }
        ];
        edges = new vis.DataSet(edgesArray);

        // create a network
        var container = document.getElementById('mynetwork');
        var data = {
            nodes: nodes,
            edges: edges
        };

        var options = {
            physics: {
                enabled: false
            },
            edges: {
                dashes: true, smooth: {
                    enabled: false
                }
            },
            groups: {
                nodes: {
                    shape: 'circle'
                },
                sensors: {
                    shape: 'box',
                    color: sensorColor
                }
            }
        };

        network = new vis.Network(container, data, options);
        //network.addEventListener('selectNode', connectNode);
        network.addEventListener('doubleClick', dblclick);
        network.addEventListener('deselectNode', deselectNode);
    }

    function dblclick(data){
        console.log('dblclick');
        //addNode(data.pointer.canvas.x, data.pointer.canvas.y);
    }

    //Select node or add node to canvas if not already in network
    function nodeSelect(data){
        console.log(data.id + 'selected');
        var nodesWithId = nodes.get({ filter: function (item) { return item.id == data.id;}});
        if(nodesWithId.length!=0){
            network.selectNodes(data.id);
            return;
        }

        //Create Node
        //TODO add node on next click instead of at fixed locale
        addNode(data.id, data.group, data.label, 200, -200);
    }

    function activateCurrentNode(){
        var selectedNodeIds = network.getSelectedNodes();
        if(selectedNodeIds==0){return;}
        setNodeColor(selectedNodeIds[0], activatedColor);
        $.post('/', {command: 'Activate Node', node: selectedNodeIds[0]});
    }

    function deactivateNode(nodeId){
        nodes.update({
            id: nodeId,
            color: null //null color means that the node will use group default
        });
    }

    //Set specific node color
    //nodeId: ID as stored in nodes DataSet
    //Color should contain { background, border, highlight{ background, color } as hex strings
    function setNodeColor(nodeId, color){
        nodes.update({
            id: nodeId,
            color: color
        });
    }

    //Add a node at this location
    function addNode(id, group, label, x, y) {
        console.log('Add Node');
        nodes.add({id:id, group: group,  label: label, x: x, y: y});
    }

    //Fires when a node is deselected
    function deselectNode(data){
        if(data.nodes.length == 0){console.log('No selection'); return;}
        //if a new node was selected at same time connect the nodes
        connectNodes(data.previousSelection.nodes[0], data.nodes[0]);
    }

    //Connects two nodes using IDs
    function connectNodes(from, to){
        //Get all edges that go to and from these two nodes
        console.log('Attempt to connect : ' + from + " : " + to);
        var edgesExist = edges.get({ filter: function (item) { return ((item.from == from && item.to == to) || (item.from == to && item.to  == from)); }});
        console.log('Already Existing edges : ' + edgesExist);
        //If edge already exists return
        if(edgesExist != 0){return;}
        //Add edge to list
        edges.add({id: 'e'+edges.length+1, from: from, to: to});
    }

    function changeOptions() {
        shadowState = !shadowState;
        network.setOptions({nodes:{shadow:shadowState},edges:{shadow:shadowState}});
    }

    function resetAllNodes() {
        nodes.clear();
        edges.clear();
        nodes.add(nodesArray);
        edges.add(edgesArray);
    }

    function resetAllNodesStabilize() {
        resetAllNodes();
        network.stabilize();
    }

    function setTheData() {
        nodes = new vis.DataSet(nodesArray);
        edges = new vis.DataSet(edgesArray);
        network.setData({nodes:nodes, edges:edges})
    }

    function resetAll() {
        if (network !== null) {
            network.destroy();
            network = null;
        }
        startNetwork();
    }

    startNetwork();
