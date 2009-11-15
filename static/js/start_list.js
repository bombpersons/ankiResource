dojo.require("dojo.dnd.Source");

function handle_dnd_drop(source, nodes, copy, target) {
	if(dojo.dnd.manager().target !== this){
		return;
	}

	console.log("dropped!");
	
	if (!copy) {
		precalc_sentence_map(source);
	}
	
	var old_sentence_map = target.sentence_map;
	precalc_sentence_map(target);
	var new_sentence_map = target.sentence_map;

	var changed_sentences = [];
	
	for (i in new_sentence_map) {
		if (!(i in old_sentence_map)) {
			changed_sentences.push(i);
		}
	}
	
	var sentences_string = "";
	for(var i = 0; i < changed_sentences.length; ++i){
		sentences_string = sentences_string + " " + changed_sentences[i]; 
	}
	
	if (copy) {
		update_server_copy(this.list_id, sentences_string);
	}
	else {
		update_server_move(source.list_id, this.list_id, sentences_string);
	}
	
}

function update_server_move(source_list_id, dest_list_id, changed_sentences) {
	console.log(changed_sentences);
	console.log(" moved from " + source_list_id + " to " + dest_list_id);
	
	var POSTcontent = [];
	POSTcontent["action"] = "move";			
	POSTcontent["source"] = source_list_id;
	POSTcontent["dest"] = dest_list_id;
	POSTcontent["sentences"] = changed_sentences;
	
	xhrArgs={
		url: "/manager/ajax/modify/",
		handleAs: "text",
		content: POSTcontent,
		
		load: function(data,args){
        	console.log("success");
		},
		
		// if any error occurs, it goes here:
		error: function(error,args){
			console.warn("error!",error);
		},
	}
	
	dojo.xhrPost(xhrArgs);
	
	
}

function update_server_copy(dest_list_id, changed_sentences) {
	console.log(changed_sentences);
	console.log(" copied to " + dest_list_id); 
	
	var POSTcontent = [];
	POSTcontent["action"] = "copy";			
	POSTcontent["dest"] = dest_list_id;
	POSTcontent["sentences"] = changed_sentences;
	
	xhrArgs={
		url: "/manager/ajax/modify/",
		handleAs: "text",
		content: POSTcontent,
		
		load: function(data,args){
        	console.log("success");
		},
		
		// if any error occurs, it goes here:
		error: function(error,args){
			console.warn("error!",error);
		},
	}
	
	dojo.xhrPost(xhrArgs);
}

function create_dnd_from_list(response_data, list_id) {
	var list_name = "list_" + list_id;
	var dnd_dom = create_dnd_dom(list_name, response_data[1]); 
	//response_data[0] has the list name, response_data[1] is the array of sentences in json format
	var dnd_source = new dojo.dnd.Source(dnd_dom, {accept: ["editable"], creator:custom_creator});
	dnd_source.checkAcceptance = custom_checkAcceptance;
	dnd_source.insertNodes(false, response_data[0]);
	dnd_source.list_id = list_id;
	precalc_sentence_map(dnd_source);
	dojo.connect(dnd_source, "onDndDrop", handle_dnd_drop);
}

function precalc_sentence_map(source) {
	//for each item in source.map, extracts item.data.sentence into source.sentence_map
	console.log("precalculating");
	var dict_array = {};
    source.forInItems( function (item) {	//source.map accessed through this function
        dict_array[item.data.sentence]=1;
    });
    
    source.sentence_map = dict_array;
}

function get_list(list_id) {

	var xhrArgs = {
		url: "/manager/ajax/list/get/" + list_id,
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
	node.innerHTML = item.data + item.sentence;	//debug to see sentence-id of each sentence
	//node.id = dojo.dnd.getUniqueId();
	return {node: node, data: item, type: item.type};	
//The default creator seems to set data: item.data, throwing away the "sentence" field, hence a custom creator is used here.
};

custom_checkAcceptance = function(source, nodes) {

			
	for(var i = 0; i < nodes.length; ++i){
		var sentence_id = source.getItem(nodes[i].id).data.sentence;
		//console.log(sentence_id);
		//console.dir(this.sentence_map);
		if(sentence_id in this.sentence_map) {
			//console.log("collision");
			return false;
		}
	}
	return true;
}	
