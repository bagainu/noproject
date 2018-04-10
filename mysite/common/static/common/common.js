$(document).ready(function(){
    // user votes
	$(document).on("click", "#user-votes-up", function(event){
        event.preventDefault();
        vote_button = $(this);
        vote_button.addClass("disabled");
        $.ajax({
            url: vote_button.attr("href"),
			type: "POST",
			success: function(data){
                if (data["count"] != -1){
                    vote_button.text("+ " + data["count"].toString());
                }
            }
        });
    });
    // end user votes

    // user follow and unfollow in profile page 
    var unfollow_url = null;
    var unfollow_success_callback = null;
    $(document).on("click", "#follow-toggle", function(event){
        event.preventDefault();
        follow_toggle = $(this);
        if (follow_toggle.hasClass("active")){
            // unfollow
            unfollow_url = $("#ajax-unfollow-url").attr("href");
            console.info(unfollow_url);
            unfollow_success_callback = function(data){
                if (data["return_id"] != -1){
                    follow_toggle.html('<i class="fa fa-check"></i> Follow');
                    follow_toggle.removeAttr("data-toggle", "data-target");
                    follow_toggle.removeClass("active");
                }
            }
        } else {
            // follow
            $.ajax({
                url: $("#ajax-follow-url").attr("href"),
			    type: "POST",
			    success: function(data){
                    if (data["return_id"] != -1){
                        follow_toggle.html('<i class="fa fa-times"></i> Unfollow');
                        follow_toggle.attr({"data-toggle": "modal", "data-target": "#unfollow-confirm-modal"});
                        follow_toggle.addClass("active");
                    }
                }
            });
        }
    });

    $(document).on("click", "#unfollow-btn", function(event){
        event.preventDefault();
        unfollow_btn = $(this);
        unfollow_url = unfollow_btn.attr("href");
        unfollow_success_callback = function(data){
            if (data["return_id"] != -1){
                unfollow_btn.parent().parent().parent().remove();
            }
        }
    });

	var unfollow_confirm_button = $("#unfollow-confirm-modal").find(".btn-confirm");
	unfollow_confirm_button.click(function(){
		$.ajax({
			url: unfollow_url,
			type: "POST",
			success: unfollow_success_callback 
		});
	});
    // end of user follow and unfollow in profile page 
});