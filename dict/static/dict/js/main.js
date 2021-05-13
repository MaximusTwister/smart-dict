$(document).ready( () => {

    console.log('Main.js Started')


    // Add Word from Telegram to Web Page View
    setInterval( () => {
        let current_location = $(location).attr('pathname')
        console.log('Location:', current_location)

        if (current_location === '/') {
            $.ajax({
            dataType: 'json',
            url: 'bot_handler/',
            type: "GET",
            success: (response) => {
                console.log('Success Card Update with Response:', response)
                $.each(JSON.parse(response), (i, val) => {
                    if ($('#botWordDiv_' + val.pk).length === 0) {
                        console.log('New Object Detected', val.pk)
                        document.location.href = '/'
                    }
                })
                if (response.result === false) {
                    console.log('Not Success Card Update')
                }
                }
            })
        }
    }, 5000)


    // Save New Word Modal Window Handler
    $(function(){
        let modal_window = $('#newWordModal')
        modal_window.modal({
            show:true,
            backdrop:'static'
        });

        $('#newWordBtn').click( () => {
            modal_window.modal('show');
        })

        $('#modalCloseBtn').click( () => {
            modal_window.modal('hide');
        })

        $('#modalSaveBtn').click( (e) => {
            const form = $(e.target).closest('form')
            const inputs = $("#" + word_id +" > textarea")
            inputs.prop( "disabled", true )

            const csrfmiddlewaretoken = $("#" + word_id + " > input[name=csrfmiddlewaretoken]").val()
            const data = {
                word_foreign: inputs.eq(0).val(),
                word_native: inputs.eq(1).val(),
                context_foreign: inputs.eq(2).val(),
                context_native: inputs.eq(3).val(),
            }

            $.ajax({
                headers: { "X-CSRFToken": csrfmiddlewaretoken },
                dataType: 'json',
                url: form.attr('action'),
                data: JSON.stringify(data),
                type: "POST",
                success: (response) => {
                    console.log('Success Card Update:', response)
                    if (response.result === false) {
                        console.log('Not Success Card Update')
                    }
                }
            })
            modal_window.modal('hide');
        })
    });



    // JQueryFlip v1.1.1
    $("#learnCard").flip();
    $("#learnCard").click( () => {
        console.log('Audio Toggle')
        $('#audioOne').toggle()
        $('#audioTwo').toggle()
    })



    // Score Slider Handler
    $('#scoreSlider').on('input change', '', () => {
        $('#scoreSliderValue').text($('#scoreSlider').val())
    })




    // Next Word Handler
    $('[id^="nextBtn_"]').click( (e) => {
        console.log('Save Button Clicked')

        let word_id = e.target.id.split('_')[1]
        const form = $(e.target).closest('form')

        const csrfmiddlewaretoken = $("#" + word_id + " > input[name=csrfmiddlewaretoken]").val()
        const data = {
            word_id: word_id,
            score: $('#scoreSlider').val(),
            set_initial: false,
        }

        $.ajax({
            headers: { "X-CSRFToken": csrfmiddlewaretoken },
            dataType: 'json',
            url: form.attr('action'),
            data: JSON.stringify(data),
            type: "POST",
            success: (response) => {
                console.log('Success Card Update with Response:', response)
                document.location.href = '../' + response['addr']
                if (response.result === false) {
                    console.log('Not Success Card Update')
                }
            }
        })
    })




    // Show Dictionary's Words and Buttons
    const toggleButtons = (word_id) => {
        ["#editBtn_", "#saveBtn_", "#discardBtn_"].forEach((el) => {
            $(el + word_id).toggle()
        })
    }

    $('[id^="editBtn_"]').click( (e) => {
        let word_id = e.target.id.split('_')[1]
        console.log('Edit Button Clicked: ', word_id)
        toggleButtons(word_id)
        $("#" + word_id + " > textarea").prop( "disabled", false )
    })

    $('[id^="discardBtn_"]').click( (e) => {
        let word_id = e.target.id.split('_')[1]
        console.log('Discard Button Clicked: ', word_id)
        toggleButtons(word_id)
        $("#" + word_id + " > textarea").prop( "disabled", true )
    })

    $('[id^="saveBtn_"]').click( (e) => {
        console.log('Save Button Clicked')
        let word_id = e.target.id.split('_')[1]
        toggleButtons(word_id)

        const form = $(e.target).closest('form')
        const inputs = $("#" + word_id +" > textarea")
        inputs.prop( "disabled", true )

        const csrfmiddlewaretoken = $("#" + word_id + " > input[name=csrfmiddlewaretoken]").val()
        const data = {
            word_foreign: inputs.eq(0).val(),
            word_native: inputs.eq(1).val(),
            context_foreign: inputs.eq(2).val(),
            context_native: inputs.eq(3).val(),
            set_initial: false,
        }

        $.ajax({
            headers: { "X-CSRFToken": csrfmiddlewaretoken },
            dataType: 'json',
            url: form.attr('action'),
            data: JSON.stringify(data),
            type: "POST",
            success: (response) => {
                console.log('Success Card Update:', response)
                if (response.result === false) {
                    console.log('Not Success Card Update')
                }
            }
        })
    })
});
