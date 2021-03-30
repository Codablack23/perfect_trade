const regex = /[a-z]+/
const regex_1 = /[0-9]+/
const regex_2 = /\W+/
let link_val = ""
let dollar_rate = 382
var public_key = ""
var api_key = ""



$(document).ready(() => {
    $.ajax({
        url: 'api_keys',
        dataType: "JSON",
        type: "POST",
        success: (data) => {
            api_key = data.api_key
            public_key = data.public_key

            $.ajax({
                url: `https://free.currconv.com/api/v7/convert?q=USD_NGN,NGN_USD&compact=utra&apiKey=${api_key}`,
                dataType: "JSON",
                success: (data) => {
                    console.log(data)
                    dollar_rate = Math.floor(1 * data.results.USD_NGN.val)
                        // console.log(dollar_rate)
                },
            })
        },
    })

    const loadbalance = () => {
        $.ajax({
            beforeSend: () => {
                // document.getElementById('').innerHTML

                $(`
              <div class='spinner w3-center'>
                        <div></div>
                        <div></div>
                     </div>
                   `).appendTo("#balance-status")

            },
            complete: () => {
                $('#balance-status').empty()
            },
            url: '/balance',
            type: "POST",
            success: (data) => {
                bal = JSON.parse(data)
                    // console.log(JSON.parse(data))
                $("#bal").replaceWith(`
                <h1 class="w3-animate-opacity" id="bal"><span id="bal_currency">${bal.currency}</span> <span class="bal">${bal.balance}</span></h1>
                `)
            },
            error: (err) => {
                // console.log(err)
            }
        })
    }
    const loadInvestments = () => {
        $.ajax({
            url: '/investments',
            type: "POST",
            beforeSend: () => {
                $(`
              <div class='spinner-md w3-center w3-center'>
                        <div class="red"></div>
                        <div class="red"></div>
                     </div>
                   `).appendTo("#investment_loader")

            },
            complete: () => {
                $('#investment_loader').empty()
            },
            success: (response_data) => {
                const data = JSON.parse(response_data)
                var elements = ""
                var total = 0
                var currency = "USD"
                data.investments.forEach((i) => {
                    elements += `
                 <li class="w3-animate-opacity"><span class="w3-right"><span>${i.amount}</span> <span>${i.currency}</span></span> <span class="">${i.date_invested}</span></li>
                 `
                    total += i.amount
                    currency = i.currency
                })
                $("#investment_list").replaceWith(`
                  <ul class="w3-ul">
                  ${elements}  
                  </ul>
                `)
                $('#total').replaceWith(`<li class="w3-light-grey w3-text-grey w3-animate-opacity"id="total"><span>Total</span> <span class="w3-right">${total} ${currency} </span></li>`)
            },
            error: (err) => {
                // console.log(err)
            }
        })
    }
    const loadAccount = () => {
        $.ajax({
            url: '/account',
            type: "POST",
            success: (data) => {
                // console.log(JSON.parse(data))
            },
            error: (err) => {
                // console.log(err)
            }
        })
    }
    const loadRequestedWithdraws = () => {
        $.ajax({
            beforeSend: () => {
                let spinner_elem = `
                <div class="spinner">
                 <div></div>
                 <div></div>    
                </div>
                `
                $(spinner_elem).appendTo('.loader')
                $(`
                <div class="spinner-md">
                 <div class="red"></div>
                 <div class="red"></div>    
                </div>
                `).appendTo('#withdraw_loader')
            },
            complete: () => {
                $('.loader').empty()
                $('#withdraw_loader').empty()
            },
            url: '/requested_withdraws',
            type: "POST",
            success: (data) => {
                var tr = ""
                var withdraw_list = ""
                var total = 0
                var curr = "USD"
                    // console.log(data)
                data.withdraws.forEach((withdraw) => {
                        tr += `
                   <tr>
                    <td>${withdraw.amount}</td>
                    <td>${withdraw.currency}</td>
                    <th>${withdraw.date}</th>
                    <td><button class="w3-pale-yellow btn w3-text-yellow">${withdraw.status}</button></td>
                </tr>
                   `
                        withdraw_list += `<li class="w3-animate-opacity"><span class="w3-right"><span>${withdraw.amount}</span> <span>${withdraw.currency}</span></span> <span class="">${withdraw.date}</span></li>`
                        curr = withdraw.currency
                        total += withdraw.amount
                    })
                    // console.log(tr)
                $('#tb-content').replaceWith(`
                <tbody class="w3-animate-opacity" id="tb-content">
                   ${tr}
                </tbody>   `)
                $('#withdraw_list').replaceWith(`
                <ul class="w3-ul w3-animate-opacity" id="withdraw_list">
               ${ withdraw_list}
                </ul>`)
                $('#withdraw_total').replaceWith(`<li class="w3-light-grey w3-text-grey w3-animate-opacity" id="withdraw_total"><span>Total</span> <span class="w3-right">${total} ${curr}</span></li>`)
            },
            error: (err) => {

            }
        })
    }
    const sendWithdraws = () => {
        event.preventDefault()
        amount = document.querySelector('#amount').value
        currency = document.querySelector('#currency').value

        $.ajax({
            beforeSend: () => {
                $(`
                     <div class='spinner w3-center'>
                        <div></div>
                        <div></div>
                     </div>
                   `).appendTo('#withdraw-status')
            },

            url: '/request_withdraw',
            type: "POST",
            data: {
                amount,
                currency
            },
            dataType: "JSON",
            success: (data) => {
                // console.log(data)
                if (data.status == "success") {
                    $('#withdraw-status').empty()
                    $('#withdraw-status').replaceWith(`
                    <div class="w3-animate-opacity" id="withdraw-status">
                        <div class="w3-text-green w3-pale-green p-4 ml-4 mr-4 w3-center w3-animate-opacity" style="border-radius: 13px;" id="success">
                            <h6>Request Successfull Our Admin Will Validate Your Request And Get Back To You</h6>
                        </div>
                   </div><br>
                    `)
                } else {
                    $('#withdraw-status').replaceWith(`
                      <div class="w3-animate-opacity" id="withdraw-status">
                         <div class="w3-text-red w3-pale-red p-2 ml-4 mr-4 w3-center w3-animate-opacity" style="border-radius: 13px;" id="success">
                            <h6>An Error Has Occured</h6>
                          </div>
                     </div><br>
                    `)
                }
                document.querySelector('#amount').value = null

            },
            error: (err) => {
                document.getElementById('withdraw-status').innerHTML = `
                         <div class="w3-text-red+- w3-pale-red p-2 ml-4 mr-4 w3-center w3-animate-opacity" style="border-radius: 13px;" id="success">
                            <h3>An Error Has Occured</h3>
                          </div><br>
                    `
            }
        })
    }
    const updateAccount = () => {
        event.preventDefault()
        account_name = document.querySelector('#account_name').value
        account_number = document.querySelector('#account_no').value
        country = document.querySelector('#country').value
        bank = document.querySelector('#bank').value

        $.ajax({
            beforeSend: () => {
                $(`
                     <div class='spinner w3-center'>
                        <div></div>
                        <div></div>
                     </div>
                   `).appendTo('#withdraw-status')
            },

            url: 'accounts',
            type: "POST",
            data: {
                account_name,
                account_number,
                country,
                bank
            },
            dataType: "JSON",
            success: (data) => {
                // console.log(data)
                if (data.Success == "True") {
                    $('#withdraw-status').empty()
                    $('#withdraw-status').replaceWith(`
                    <div class="w3-animate-opacity" id="withdraw-status">
                        <div class="w3-text-green w3-pale-green p-4 ml-4 mr-4 w3-center w3-animate-opacity" style="border-radius: 13px;" id="success">
                            <h6>Your Account Has Been Updated. Refresh Page To See Changes</h6>

                        </div>
                   </div><br>
                    `)
                } else {
                    $('#withdraw-status').replaceWith(`
                      <div class="w3-animate-opacity" id="withdraw-status">
                         <div class="w3-text-red w3-pale-red p-2 ml-4 mr-4 w3-center w3-animate-opacity" style="border-radius: 13px;" id="success">
                            <h6>An Error Has Occured</h6>
                          </div>
                     </div><br>
                    `)
                }

            },
            error: (err) => {
                document.getElementById('withdraw-status').innerHTML = `
                         <div class="w3-text-red w3-pale-red p-4 ml-4 mr-4 w3-center w3-animate-opacity" style="border-radius: 13px;" id="success">
                            <h3>An Error Has Occured</h3>
                          </div><br>
                    `
            }
        })
    }
    loadInvestments()
    loadAccount()
    loadRequestedWithdraws()



    $('#side-btn').click(() => {
            $('#sidebar').animate({
                width: 'toggle'
            })
            $('.w3-overlay').toggle()

        }),
        $('.w3-overlay').click(() => {
            $('#sidebar').animate({
                    width: 'toggle'
                }),
                $('.w3-overlay').toggle()

        }),

        $('#open_plans').click(() => {
            $('#open_plans').toggleClass("glyphicon-chevron-down")
            $('#open_plans').toggleClass("glyphicon-chevron-up")
            $('#closed_plans').slideToggle()
        }),
        $("#logout").click(() => {
            $('#confirm_logout').slideDown()
        }),
        $('#cancel').click(() => {
            $('#confirm_logout').slideUp()
        }),

        //     $('#reff').ready(() => {
        //         const val = document.querySelector('#copied-text').value
        //         link_value = `${location.origin}/signup/${val}`
        //         document.querySelector('#copied-text').value = link_value
        //     })
        // $('#copy-button').click(() => {
        //         console.log(location)
        //         let copied_text = document.querySelector('#copied-text')
        //         copied_text.select()
        //         document.execCommand('copy')
        //         $("#link_copied").fadeIn().fadeOut(4000)

        //     }),
        $('#withdraw_form').submit(sendWithdraws),
        $('#refresh-balance').click(loadbalance)
    $('#refresh-table').click(loadRequestedWithdraws)
    $('#more_investment').click(loadInvestments)
    $('#more_withdraws').click(loadRequestedWithdraws)
    $('#account_form').submit(() => {
        event.preventDefault()
        updateAccount()
    })
    var error = {
        new_pass: "",
        confirm_pass: ""
    }
    const validate = (np) => {
        if (regex.test(np) && regex_1.test(np) && regex_2.test(np)) {
            new_err = ""
            error['new_pass'] = new_err
        } else {
            new_err = "your must contain a number and a special character"
            error['new_pass'] = new_err
        }

        $('#new_password_err').text(new_err)

    }
    const validate_confirm = (cp, np) => {

        if (cp != np) {
            confirm_err = "Passwords Do not Match"
            error['confirm_pass'] = confirm_err
        } else {
            confirm_err = ""
            error['confirm_pass'] = confirm_err
        }
        // console.log(confirm_err)
        $('#confirm_password_err').text(confirm_err)
    }
    let new_err = ""
    let confirm_err = ""
    $('#new_password').keyup(() => {
        const n_password = document.getElementById('new_password')
        const confirm = document.getElementById("confirm_new_password")



        // console.log(n_password.value)
        // if ((regex.test(n_password.value) && regex_1.test(n_password.value)) && regex_2.test(n_password.value)) {
        //     console.log('key pressed')
        // } else {
        //     console.log("your must contain a number and a special character")
        // }
        validate(n_password.value)
    })
    $('#confirm_new_password').keyup(() => {
        const n_password = document.getElementById('new_password')
        const confirm = document.getElementById("confirm_new_password")
            // console.log(n_password.value)
            // if ((regex.test(n_password.value) && regex_1.test(n_password.value)) && regex_2.test(n_password.value)) {
            //     console.log('key pressed')
            // } else {
            //     console.log("your must contain a number and a special character")
            // }
        validate_confirm(confirm.value, n_password.value)
    })
    $("#change_password_form").submit(() => {
        const n_password = document.getElementById('new_password')
        const confirm = document.getElementById("confirm_new_password")

        validate(n_password.value)
        validate(confirm.value)
        if (error['new_pass'] == "" && error['confirm_pass'] == "") {

        } else {
            event.preventDefault()
        }

    })
    let currentPlan = ""
    let minimum_value = 250
    const selectPlan = (index, plan, Name) => {
        $(`.${Name}`).eq(index).addClass("w3-pale-green w3-text-green")

        console.log($(`.${Name}`).eq(index))
        const nums = [0, 1, 2]
        const min = [270, 1000, 10000]
        for (let i = 0; i < nums.length; i++) {
            if (i != index) {
                $(`.${Name}`).eq(i).removeClass("w3-pale-green w3-text-green")

            }
        }
        minimum_value = min[index] * dollar_rate
        currentPlan = plan

        document.getElementById('payment_amount').min = minimum_value
    }


    $('.paystack_payment_form').submit(() => {
        event.preventDefault()
        if (currentPlan == "") {
            $('.check_plan').slideDown()
            setTimeout(() => {
                $('.check_plan').fadeOut(1000)
            }, 3000)
        } else {
            const email = document.querySelector('#payment_email').value
            const amount = document.querySelector('#payment_amount').value * 100
            const new_currency = document.querySelector('#payment_currency').value
            returns = amount * (5 / 10)
            let setup = PaystackPop.setup({
                key: public_key, // Replace with your public key
                email,
                amount, // the amount value is multiplied by 100 to convert to the lowest currency unit
                currency: 'NGN',
                callback: function(response) {
                    console.log(returns)
                    console.log(amount)
                    $.ajax({
                            url: 'invest',
                            dataType: "JSON",
                            data: {
                                "email": email,
                                "amount": amount,
                                "currency": new_currency,
                                "returns": amount + returns,
                                "Duration": 70,
                                "plan": currentPlan
                            },
                            type: "POST",
                            success: (result) => {
                                console.log(result)
                            },
                        })
                        //this happens after the payment is completed successfully
                        // var reference = response.reference;
                        // alert('Payment complete! Reference: ' + reference);
                        // Make an AJAX call to your server with the reference to verify the transaction
                },
                onClose: function() {

                },
            });
            setup.openIframe();
        }
    })
    $('#edit-account').click(() => {
        $('#update_account').slideToggle()
    })


})