$(document).ready(function () {
    setUpStars();
    click_rate_starts(1);
});

function setUpStars() {
    for (let i = 1; i <= 5; i++) {
        let star = $("#rate_star_" + i);
        star.hover(function () {
            hover_rate_stars(i);
        }, function () {
            hover_rate_stars(0);
        });

        star.click(function () {
            click_rate_starts(i);
        })
    }
}

function hover_rate_stars(rating) {
    for (let i = 1; i <= rating; i++) {
        let star = $("#rate_star_" + i);
        star.addClass("bordered-star");
        if (!star.hasClass("checked")) {
            star.addClass("hovered");
        }
    }
    for (let i = 5; i > rating; i--) {
        let star = $("#rate_star_" + i);
        star.removeClass("bordered-star");
        star.removeClass("hovered");
    }
}

function click_rate_starts(rating) {
    $("#ratingInput").val(rating);
    for (let i = 1; i <= rating; i++) {
        let star = $("#rate_star_" + i);
        star.addClass("checked");
        star.removeClass("hovered");
    }
    for (let i = 5; i > rating; i--)
        $("#rate_star_" + i).removeClass("checked");
}