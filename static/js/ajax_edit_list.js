	dojo.require("dojo.NodeList-fx");
	dojo.require("dijit.form.Button");
    dojo.require("dijit.form.DropDownButton");
    dojo.require("dijit.Menu");
    dojo.require("dijit.form.TextBox");

	function add_to_list(sentence_id, list_id) {
			// An array for the post data
			var POSTcontent = new Array();
			
			POSTcontent["add"] = 1;			
			POSTcontent["list"] = list_id;
			POSTcontent["sentence"] = sentence_id;
			
			xhrArgs={
				url: "/lists/ajax/list/add/",
				handleAs: "text",
				content: POSTcontent,
				
				load: function(data,args){
                	dojo.byId("response"+sentence_id).innerHTML = "Added.";
				},
				
				// if any error occurs, it goes here:
				error: function(error,args){
					console.warn("error!",error);
				},
			}
			
			dojo.xhrPost(xhrArgs);
            dojo.byId("response"+sentence_id).innerHTML = "Adding..."
	}
	
	function remove_from_list(sentence_id, list_id) {
		// An array for the post data
		var POSTcontent = new Array();
		
		POSTcontent["remove"] = 1;			
		POSTcontent["list"] = list_id;
		POSTcontent["sentence"] = sentence_id;
		
		xhrArgs={
			url: "/lists/ajax/list/add/",
			handleAs: "text",
			content: POSTcontent,
			
			load: function(data,args){
            	dojo.byId("response"+sentence_id).innerHTML = "Removed.";
			},
			
			// if any error occurs, it goes here:
			error: function(error,args){
				console.warn("error!",error);
			},
		}
		
		dojo.xhrPost(xhrArgs);
        dojo.byId("response"+sentence_id).innerHTML = "Removing..."
	}

