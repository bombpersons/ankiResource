dojo.require("dojo.NodeList-fx");

function get_sentences_from_smart_fm(word) {
		var POSTcontent = new Array();
		
		POSTcontent["word"] = word;			
		
		xhrArgs={
			url: "/sentences/smart_fm/"+word,
			handleAs: "json",
			content: POSTcontent,
			
			load: function(data,args){
            	dojo.byId("smart_fm").innerHTML = "Found X matches. <br /> <br />";
				dojo.forEach(data, function(item){
						dojo.byId("smart_fm").innerHTML += item;
						dojo.byId("smart_fm").innerHTML += "<br />";
				}
);
            	
			},

			error: function(error,args){
				console.warn("error!",error);
			},
		}
		
		dojo.xhrPost(xhrArgs);
        dojo.byId("smart_fm").innerHTML = "Getting..."
}
