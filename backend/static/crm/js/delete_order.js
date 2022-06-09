function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

$(document).ready(function () {
    $(document).click(function (event) {
        if (!$(event.target).parent().closest('.lead-menu').length) {
            $('.delete-menu').removeClass('menu-enabled')
        }
    })
    $('.delete-menu-item').click(function (event) {
        let csrftoken = getCookie('csrftoken')
        let order_card = $(event.target).parents('.lead-card__wrapper')
        let order_id = order_card.data('id')
        $.ajax({
            url: `/api/v1/delete_order/${order_id}`,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'id': 5,
            },
            method: 'DELETE',
            success: function (data) {
                let leads_counter = $('#total-leads');
                let budget_counter = $('#total-budget');
                leads_counter.text(parseInt(leads_counter.text()) - 1);
                let lead_budget = $(event.target).parents('.lead-card').find('.budget-value').text()
                budget_counter.text(parseInt(budget_counter.text()) - parseInt(lead_budget));
                order_card.remove()
            },
            error: function (xhr) {
                alert(xhr.statusText)
            }
        })
    })
    $('.lead-menu').click(function (event) {
        $(event.target).parent().find('.delete-menu').addClass('menu-enabled')
    })
})