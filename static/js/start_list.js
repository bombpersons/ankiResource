dojo.require("dojo.dnd.Source");

function create_dnd_from_list(response_data, list_id) {
	var list_name = "list_" + list_id;
	var dnd_dom = create_dnd_dom(list_name, response_data[1]); 
	//response_data[0] has the list name, response_data[1] is the array of sentences in json format
	var dnd_source = new dojo.dnd.Source(dnd_dom, {accept: ["editable"], creator:custom_creator});
	dnd_source.checkAcceptance = custom_checkAcceptance;
	dnd_source.insertNodes(false, response_data[0]);
	precalc_sentence_map(dnd_source);
}

function precalc_sentence_map(source) {
	//for each item in source.map, extracts item.data.sentence into source.sentence_map
	var dict_array = new Array();
    source.forInItems( function (item) {	//source.map accessed through this function
        dict_array.push(item.data.sentence);
    });
    
    source.sentence_map = dict_array;
    
    //console.log(4 in dict_array);
	//console.dir(source);
	
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
// this.sentence_map: 			array of items in the source
// source.getItem(nodes[i].id):	ith item in the nodes selected	
	
	var flag = true;
			
	for(var i = 0; i < nodes.length; ++i){
		var sentence_id = source.getItem(nodes[i].id).data.sentence;
		if(sentence_id in this.sentence_map) {
			console.log("collision");
		}
	}
	return true;
}	






