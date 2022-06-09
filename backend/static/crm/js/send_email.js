function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

$(document).ready(function (event) {
    let trigger_modal = $('#send-mail-trigger-modal')
    let send_mail_modal = $('.create-mail-section')
    let close_modal_btn = $('#close-mail-btn')
    let send_mail_btn = $('#send-mail-btn')
    trigger_modal.click(function (evt) {
        if (!send_mail_modal.hasClass('enabled')){
            send_mail_modal.addClass('enabled')
        }
    })
    close_modal_btn.click(function (evt) {
        send_mail_modal.removeClass('enabled')
    })
    send_mail_btn.click(function (evt) {
        let form = $(evt.target).parents('form')
        send_mail(form)
    })
})

function send_mail(form) {
    let data = form.serializeArray();
    let csrftoken = getCookie('csrftoken')
    let send_mail_modal = $('.create-mail-section')
    let send_mail_btn = $('#send-mail-btn')
    let ajaxLoader = $('.ajax-loader ')

    $.ajax({
        url: '/api/v1/send_mail',
        data: data,
        headers: {
                'X-CSRFToken': csrftoken
            },
        method: 'POST',
        beforeSend: function(){
            send_mail_btn.text('Отправка...')
            ajaxLoader.addClass('enabled')
        },
        success: function (data) {
            $(form).find('input').each(function () {
                $(this).val('')
            })
            $(form).find('textarea').val('')
            send_mail_modal.removeClass('enabled')
            ajaxLoader.removeClass('enabled')
        },
        error: function (xhr) {
            send_mail_btn.text('Ошибка отправки')
            ajaxLoader.removeClass('enabled')
        }
    })
}