$(document).ready(function(){
	$(document).on("click", "#user-votes-up", function(event){
        event.preventDefault();
        vote_button = $(this);
        vote_button.addClass("disabled");
        $.ajax({
            url: vote_button.attr("href"),
			type: "POST",
			success: function(data){
                if (data["count"] != -1)
                {
                    vote_button.text("+ " + data["count"].toString());
                }
            }
        });
    });
});