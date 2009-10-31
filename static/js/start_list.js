dojo.require("dojo.dnd.Source");

function insert_into_start_list(nodes_array) {
		var start_list = new dojo.dnd.Source("start_list_nodes");
		start_list.insertNodes(false, nodes_array);
}

function get_list(list_id) {

	var targetNode = dojo.byId("xhrget_reponse_test");

	var xhrArgs = {
		url: "/lists/ajax/list/get/" + list_id,
		handleAs: "json",
		load: function(response_data){

		insert_into_start_list(response_data);
		
	  },
	  error: function(error){
		targetNode.innerHTML = "An unexpected error occurred: " + error;
	  }
	}

	//Call the asynchronous xhrGet
	var deferred = dojo.xhrGet(xhrArgs);
}

function get_first_list() {
	get_list(1);
}

//dojo.addOnLoad(init_source);
dojo.addOnLoad(get_first_list);
