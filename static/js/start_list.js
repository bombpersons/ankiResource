dojo.require("dojo.dnd.Source");

function create_dnd_from_list(response_data, list_id) {
	var list_name = "list_" + list_id;
	var dnd_dom = create_dnd_dom(list_name, response_data[1]); 
	//response_data[0] has the list name, response_data[1] is the array of sentences in json format
	var start_list = new dojo.dnd.Source(dnd_dom, {accept: ["editable"], creator:custom_creator});
	start_list.checkAcceptance = custom_checkAcceptance;
	start_list.insertNodes(false, response_data[0]);
}

function get_list(list_id) {

	var xhrArgs = {
		url: "/lists/ajax/list/get/" + list_id,
		handleAs: "json",
		load: function(response_data){
			create_dnd_from_list(response_data, list_id);
		},
	  error: function(error){
		console.log("error!");
	  }
	}
	dojo.xhrGet(xhrArgs);
}

function create_dnd_dom(name, title) { //returns a DOMnode of the ol

	var parent = dojo.byId("dnd_area");

	target = dojo.create("div", {id: name + '_container' ,class: "dnd_list_container"}, parent);
	dojo.create("h2", {class: "list_title", innerHTML: title}, target);
	return dojo.create("ol", {id: name + "_nodes"}, target);

}

var custom_creator = function(item, hint){
	var node;
	node = dojo.doc.createElement("li");
	node.innerHTML = item.data;
	node.id = dojo.dnd.getUniqueId();
	return {node: node, data: item, type: item.type};	
//The default creator seems to set data: item.data, throwing away the "sentence" field, hence a custom creator is used here.
};

custom_checkAcceptance = function(source, nodes) {
// this.map: 					array of items in the target
// source.map: 					array of items in the source
// source.getItem(nodes[i].id):	ith item in the nodes selected
			
	console.log("this.map:");
	console.dir(this.map);
	
	console.log("source.map:");
	console.dir(source.map);

	console.log("items in nodes:");			
	for(var i = 0; i < nodes.length; ++i){
		
		var type = source.getItem(nodes[i].id).type;
		var item = source.getItem(nodes[i].id)

		console.dir(item);
	}
	return true;
}	






