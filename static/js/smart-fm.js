dojo.require("dojo.NodeList-fx");

function get_sentences_from_smart_fm(word) {
		var POSTcontent = new Array();
		
		POSTcontent["word"] = word;			
		
		xhrArgs={
			url: "/sentences/smart_fm/"+word,
			handleAs: "json",
			content: POSTcontent,
			
			load: function(data,args){
            	dojo.byId("response").innerHTML = "Got it.";
            	dojo.byId("smart_fm").innerHTML = data["smart_fm_sentence"];
			},

			error: function(error,args){
				console.warn("error!",error);
			},
		}
		
		dojo.xhrPost(xhrArgs);
        dojo.byId("response").innerHTML = "Getting..."
}
