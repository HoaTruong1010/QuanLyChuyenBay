$(document).ready(function() {
    $('#medium1, #medium2').hide()

    $('input[type=checkbox][name=isMedium]').on('change', function() {
        if ($(this).is(":checked"))
            $('input[type=radio][name=flexRadioDefault]').removeAttr("disabled")
        else {
            $('input[type=radio][name=flexRadioDefault]').prop({
                "checked": false,
                "disabled": true
            })

            $('#medium1, #medium2').hide()
            removeTemplate()
        }
    })

    $('.form-check-input[type=radio]').on('change', function() {
        var number = $('.form-check-input[type=radio]:checked').val()
        if (number == "1") {
            $('#medium1').show()
            $('#medium2').hide()
        }
        else {
            $('#medium1, #medium2').show()
        }
    })
})