$(document).ready(function() {
    $(".edit_category_btn").hide()
    $(".remove_category_btn").hide()
    $(".edit_category_name").hide()

    $('#redact_btn').on('click', function() {
      if (!$(this).hasClass('clicked')) {
        $(this).addClass('clicked');
        $(".edit_category_btn").show()
        $(".remove_category_btn").show()
        $(".category_count").hide()
        $(".category_arrow").hide()
      } else {
        $(this).removeClass('clicked');
        $(".edit_category_btn").hide()
        $(".remove_category_btn").hide()
        $(".category_count").show()
        $(".category_arrow").show()
        $(".category_name").show()
        $(".edit_category_name").hide()
      }
    });

    $('li .edit_category_btn ').on('click', function() {
      if (!$(this).hasClass('clicked')) {
        $(this).addClass('clicked');
        $(".edit_category_name").show()
        $(".category_name").hide()
      } else {
        $(this).removeClass('clicked');
        $(".edit_category_name").hide()
        $(".category_name").show()
      }
    });
    $(".edit_reminder_form").hide()
    $('li #edit_reminder_btn ').on('click', function() {
      if (!$(this).hasClass('clicked')) {
        $(this).addClass('clicked');
        $(".edit_reminder_form").show()
        $(".reminder_name").hide()
        $(".reminder_datetime").hide()
      } else {
        $(this).removeClass('clicked');
        $(".edit_reminder_form").hide()
        $(".reminder_name").show()
        $(".reminder_datetime").show()
      }
    });

});