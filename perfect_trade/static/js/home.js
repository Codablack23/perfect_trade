$(document).ready(() => {
    $('#show_bronze').click(() => {
            $('#hidden-message-bronze').slideToggle()
        }),
        $('#show_silver').click(() => {
            $('#hidden-message-silver').slideToggle()
        }),
        $('#show_gold').click(() => {
            $('#hidden-message-gold').slideToggle()
        }),
        $('#show_diamond').click(() => {
            $('#hidden-message-diamond').slideToggle()
        })
    let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    numbers.forEach(number => {
        $('#more-' + number).click(() => {
            $('.answers-' + number).slideToggle()

        })
    })
})
const form_errors = {
    email: "",
    firstname: "",
    lastname: "",
    subject: "",
    message: ""
}
let message_error = ""
const validators = {
    email: (target) => {

    },
    firstname: (target) => {
        if (target.value == "" || target.value == "") {
            form_errors[target.id] = 'Please Fill Out This Field'
        } else {
            if (target.value.length < 3) {
                form_errors[target.id] = 'Firstname Must Be Atleast 3 characters'
            } else {
                const regex = /[a-z/A-Z]+$/
                if (regex.exec(target.value)) {
                    form_errors[target.id] = ""
                } else {
                    form_errors[target.id] = "firstname Must Contain alphabets Only"
                }
            }
        }
        document.getElementById(`${target.id}-error`).innerHTML = form_errors[target.id]
    },
    lastname: (target) => {
        if (target.value == "" || target.value == " ") {
            form_errors[target.id] = 'Please Fill Out This Field'
        } else {
            if (target.value.length < 3) {
                form_errors[target.id] = 'Lastname Must Be Atleast 3 characters'
            } else {
                const regex = /[a-z/A-Z]+$/
                if (regex.exec(target.value)) {
                    form_errors[target.id] = ""
                } else {
                    form_errors[target.id] = "Lastname Must Contain alphabets Only"
                }
            }
        }
        document.getElementById(`${target.id}-error`).innerHTML = form_errors[target.id]
    },
    subject: (target) => {
        if (target.value == "" || target.value == " ") {
            form_errors[target.id] = 'Please Fill Out This Field'
        } else {
            if (target.value.length < 3) {
                form_errors[target.id] = 'Your Subject Must Be Atleast 3 characters'
            } else {
                const regex = /[a-z/A-Z/ ]+$/
                if (regex.exec(target.value)) {
                    form_errors[target.id] = ""
                } else {
                    form_errors[target.id] = "Subject Must Contain Letters and Whitespace"
                }
            }
        }
        document.getElementById(`${target.id}-error`).innerHTML = form_errors[target.id]
    },
    message: (target) => {
        if (target.value == "" || target.value == " ") {
            form_errors[target.id] = 'Please Fill Out This Field'
        } else {
            if (target.value.length < 3) {
                form_errors[target.id] = 'Your Message Must Be Atleast 3 characters'
            } else {
                const regex = /[a-z/A-Z/ ]+$/
                if (regex.exec(target.value)) {
                    form_errors[target.id] = ""
                } else {
                    form_errors[target.id] = "Message Must Contain Letters and Whitespace"
                }
            }
        }
        document.getElementById(`${target.id}-error`).innerHTML = form_errors[target.id]
    },
}
let values = document.querySelectorAll('input')
    // ajax request to submit contact
values.forEach((value) => {
    value.addEventListener('input', (e) => {
        const target = e.target
        validators[target.id](target)
    })
})
document.getElementById('message').addEventListener('input', (e) => {
    target = e.target
    validators[target.id](target)
})
$(document).ready(() => {
    $('#contact-form').submit(() => {
        event.preventDefault()
        let {
            email,
            firstname,
            lastname,
            subject,
            message
        } = form_errors
        const error_array = [email, firstname, lastname, subject, message]

        const is_validated = error_array.filter((arr) => {
            return arr != ""
        })
        if (is_validated.length > 0) {
            console.log(is_validated)
        } else {
            messages = {

            }
            console.log(messages)
            let message = document.querySelector('textarea').value
            messages['message'] = message
            values.forEach((val) => {
                messages[val.id] = val.value
            })
            event.preventDefault()
            $.ajax({
                url: "/contact",
                type: "POST",
                dataType: "text",
                data: messages,
                success: (data) => {
                    const status = JSON.parse(data)
                    if (status.status == "success") {
                        $("#success").slideDown()
                    } else {
                        $("#failed").slideDown()
                    }

                },
                error: () => {
                    $("#failed").slideDown()
                }

            })

        }

    })
    $('#failed-close-btn').click(() => {
            $('#failed').slideUp()
        }),
        $('#success-close-btn').click(() => {
            $('#success').slideUp()
        })

    $("#hide-portfolio").click(() => {
        $('#hidden-portfolio').slideToggle()
        $('#main-portfolio').slideToggle()
    })
    $("#show-portfolio").click(() => {
        $('#hidden-portfolio').slideToggle()
        $('#main-portfolio').slideToggle()
    })
    $("#hide-portfolio-1").click(() => {
        $('#hidden-portfolio-1').slideToggle()
        $('#main-portfolio-1').slideToggle()
    })
    $("#show-portfolio-1").click(() => {
        $('#hidden-portfolio-1').slideToggle()
        $('#main-portfolio-1').slideToggle()
    })
})