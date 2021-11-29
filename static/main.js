$(document).ready(()=>{
    console.log('The new javascript my friend.. not im lying')
    $('#modal-btn').click(function(){
        console.log('working')
        $('.ui.modal')
        .modal('show')
        ;
    })
    $('.ui.dropdown').dropdown()
})