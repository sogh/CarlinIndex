        $(function() {  
        	  $("#btn").click(function() {  
        		  var userName = $("#prependedInput").val()
        		  $.ajax({  
        			  type: "POST",  
        			  url: "/user",  
        			  data: {name: "" + userName + ""},
        			  datatype: "json",
        			  error: function(jqXHR, textStatus, errorThrown) {  
        	alert("fail")},  
			  success: function(data) {  
				  $.each(data, function(index, user) {
		        	if(userName == user.name)
		        		{
		        		$("p").text(user.topTweet)
		        		$("small").text(user.name)
		        		}
					  $("#tr" + index).children('td').eq(1).text(user.name)	
					  $("#tr" + index).children('td').eq(2).text(user.carlinIndex)	
					  $("#tr" + index).children('td').eq(3).text(user.topTweet)})
					  
		        	} 
        			});  
        	  });  
        	});  
        
        $(function() {  
        	$("table").tablecloth({
        		  theme: "dark",
        		  bordered: true,
        		  condensed: true,
        		  clean: true,
        		});
        })
        
        $(function() {  
        	 $.ajax({  
   			  type: "GET",  
   			  url: "/users",  
   			  datatype: "json",
   			  error: function(jqXHR, textStatus, errorThrown) {  
   	alert("fail")},  
		  success: function(data) {  
			  $.each(data, function(index, user) {
				  $("#tr" + index).children('td').eq(1).text(user.name)	
				  $("#tr" + index).children('td').eq(2).text(user.carlinIndex)	
				  $("#tr" + index).children('td').eq(3).text(user.topTweet)})
				  
	        	} 
   			});  
        })