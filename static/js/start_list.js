dojo.require("dojo.dnd.Source");

function get_list(list_id) {

	var xhrArgs = {
		url: "/lists/ajax/list/get/" + list_id,
		handleAs: "json",
		load: function(response_data){

		var list_name = "list_" + list_id;
		var ol_t = create_dnd_target(list_name, response_data[1]); 
		var start_list = new dojo.dnd.Source(ol_t);
		
		start_list.insertNodes(false, response_data[0]);
		
		
	  },
	  error: function(error){
		targetNode.innerHTML = "An unexpected error occurred: " + error;
	  }
	}

	//Call the asynchronous xhrGet
	var deferred = dojo.xhrGet(xhrArgs);
}

function create_dnd_target(name, title) { //returns a DOMnode of the ol

	var parent = dojo.byId("dnd_area");

	target = dojo.create("div", {id: name + '_container' ,class: "dnd_list_container"}, parent);
	dojo.create("h2", {innerHTML: title}, target);
	return dojo.create("ol", {id: name + "_nodes"}, target);

}








