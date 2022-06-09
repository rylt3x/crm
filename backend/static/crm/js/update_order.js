function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Ивенты на клик
$(document).ready(function () {
    // Сохранение DOM элементов в переменные
    let createTaskButton = $("#create-task")
    let deleteTaskButton = $('.task-delete-btn')
    let completeTaskButton = $('.task-complete-btn')
    let taskInput = $('#id_task_name')

    // Ивент на нажатие CTRL+Enter
    taskInput.on('keypress', create_task_on_enter)

    // Ивент на отправку задачи или коммента
    createTaskButton.click(function (event) {
        let form = $('#task-form')
        create_task(form)
    })

    // Ивенты на кнопки Удалить задачу и Выполнить
    deleteTaskButton.click(delete_task)
    completeTaskButton.click(complete_task)

    // Удалить класс invalid с инпута текста задачи при расфокусе
    taskInput.blur(function (event) {
        if ($(event.target).hasClass('invalid')){
            $(event.target).removeClass('invalid')
            $(event.target).val('')
        }
    })
    // Смена параметров формы в зависимости от того, коммент или задачу мы ставим
    $('.task-or-comment-selector').on('change', change_form_params)

    // Маска номера телефона
    let phoneInput = document.getElementById('id_client_phone_number');
        let maskOpts = {
        mask: '{+7} (#00) 000-00-00',
        definitions: {
            '#': /[1-9]/
        },
    }
    let mask = new IMask(phoneInput, maskOpts)
})

// Аякс на рест эндпоинт на создание задачи
function create_task(form) {
    let data = form.serializeArray()
    let csrftoken = getCookie('csrftoken')
    let createTaskButton = $("#create-task")
    let taskTextInput = $('.task-input.task-name')
    let sendUrl = form.find('option:selected').data('url')

    $.ajax({
        url: sendUrl,
        data: data,
        headers: {'X-CSRFToken': csrftoken},
        method: 'POST',
        beforeSend: function(xhr, opts) {
            console.log(sendUrl)
            if (taskTextInput.val() === '') {
                taskTextInput.attr('placeholder', 'Введите текст')
                taskTextInput.addClass('invalid')
                xhr.abort();
                taskTextInput.focus();
                return
            }
            createTaskButton.text('Отправка...')
        },
        success: function (data) {
            setTimeout(()=>createTaskButton.text('Отправить'), 300)
            window.location.reload()
        },
        error: function (xhr) {
            createTaskButton.text('Ошибка отправки')
            console.log(xhr)
        },
    })
}

// Аякс на рест на удаление задачи
function delete_task(event) {
    let data_id = $(event.target).parents('.task-item').data('id')
    let csrftoken = getCookie('csrftoken')
    $.ajax({
        url: `/api/v1/delete_task/${data_id}`,
        method: 'DELETE',
        headers: {'X-CSRFToken': csrftoken},
        success: function (data) {
            window.location.reload()
        },
        error: function (xhr) {
            alert(xhr.statusText)
        }
    })
}

// Аякс на завершение задачи
function complete_task(event) {
    let data_id = $(event.target).parents('.task-item').data('id')
    let csrftoken = getCookie('csrftoken')
    $.ajax({
        url: `/api/v1/update_task/${data_id}`,
        method: 'UPDATE',
        headers: {'X-CSRFToken': csrftoken},
        success: function (data) {
            window.location.reload()
        },
        error: function (xhr) {
            alert(xhr.statusText)
        }
    })
}

// Отправка на ctrl-enter
function create_task_on_enter(event) {
    let keyPressed = event.code
    if (event.ctrlKey && keyPressed === "Enter"){
        let form = $('#task-form')
        create_task(form)
    }
}
// Коллбек функция на смену селектора задачи или коммента
function change_form_params(event) {
    let fieldName = $(event.target).find('option:selected').data('field-name')
    $('#id_task_name').attr('name', fieldName)
    if (fieldName === 'text'){
        $('#id_task_deadline').addClass('deadline-disabled')
    }
    else {
        $('#id_task_deadline').removeClass('deadline-disabled')
    }
}
