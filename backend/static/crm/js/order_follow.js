$(document).ready(function () {
    $('.lead-card-header').click(function (event) {
        let follow_link = $(event.target).attr('href');
        console.log(follow_link)
        window.location.href = follow_link;
    });
})