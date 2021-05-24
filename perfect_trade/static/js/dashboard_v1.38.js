const regex = /[a-z]+/
const regex_1 = /[0-9]+/
const regex_2 = /\W+/
let link_val = ""
let dollar_rate = 382
var public_key = ""
var api_key = ""

let currentPlan = ""
let minimum_value = 270
let max_value = 999
var percentage = ''


function selectPlan(index, plan, Name) {
    $(document).ready(() => {
        $(`.${Name}`).eq(index).addClass("w3-pale-green w3-text-green")

        console.log($(`.${Name}`).eq(index))
        const nums = [0, 1, 2, 3]
        const percent = [30, 45, 60, 70]
        const min = [270, 1000, 10000, 100000]
        const max = [999, 9999, 99999, 999999]
        for (let i = 0; i < nums.length; i++) {
            if (i != index) {
                $(`.${Name}`).eq(i).removeClass("w3-pale-green w3-text-green")

            }
        }
        minimum_value = min[index]
        max_value = max[index]
        currentPlan = plan
        percentage = percent[index]

        document.getElementById('payment_amount').min = minimum_value
        document.getElementById('payment_amount').max = max_value
    })
}


$(document).ready(() => {
    $('#edit-btc').click(() => {
        var btc_edit = document.querySelector('#btc-input')
        btc_edit.readOnly = false
        $('#edit-btc').fadeOut()
        $('#check_edit_btc').fadeIn()
    })
    $('#edit-ether').click(() => {
        var eth_edit = document.querySelector('#ether-input')
        eth_edit.readOnly = false
        $('#edit-ether').fadeOut()
        $('#check_edit_eth').fadeIn()
    })
    $('#check_edit_btc').click(() => {
        var btc_edit = document.querySelector('#btc-input')
        btc_edit.readOnly = true
        $('#check_edit_btc').fadeOut()
        $('#edit-btc').fadeIn()
    })
    $('#check_edit_eth').click(() => {
        var eth_edit = document.querySelector('#ether-input')
        eth_edit.readOnly = true
        $("#check_edit_eth").fadeOut()
        $('#edit-ether').fadeIn()
    })
    $('#Close_tab').click(() => {
        $('.main_form').fadeIn()
        $('.crypto_details').fadeOut()
    })
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
                if (data.investments.length > 0) {
                    data.investments.forEach((i) => {
                        if (i.payment_status == 'Paid') {

                            elements += `
                        <li class="w3-animate-opacity"><span class="w3-right"><span>${i.amount}</span> <span>${i.currency}</span></span> <span class="">${i.date_invested}</span></li>
                        `
                            total += i.amount
                            currency = i.currency
                        } else {}
                    })
                    $("#investment_list").replaceWith(`
                  <ul class="w3-ul">
                  ${elements}  
                  </ul>
                `)
                    $('#total').replaceWith(`<li class="w3-light-grey w3-text-grey w3-animate-opacity"id="total"><span>Total</span> <span class="w3-right">${total} ${currency} </span></li>`)

                } else {

                }
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
                if (data.withdraws.length > 0) {
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

                } else {


                }
            },
            error: (err) => {

            }
        })
    }
    const sendWithdraws = () => {
        event.preventDefault()
        amount = document.querySelector('#amount').value
        currency = document.querySelector('#currency').value
        w_date = document.querySelector('#withdraw_date').value


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
                currency,
                w_date
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

        $('#reff').ready(() => {
            const val = document.querySelector('#copied-text').value
            link_value = `${location.origin}/signup/${val}`
            document.querySelector('#copied-text').value = link_value
        })
    $('#copy-button').click(() => {
            console.log(location)
            let copied_text = document.querySelector('#copied-text')
            copied_text.select()
            document.execCommand('copy')
            $("#link_copied").fadeIn().fadeOut(4000)

        }),
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


    $('.paystack_payment_form').submit(() => {
        event.preventDefault()
        if (currentPlan == "") {
            $('.check_plan').slideDown()
            setTimeout(() => {
                $('.check_plan').fadeOut(1000)
            }, 3000)
        } else {
            const email = document.querySelector('#payment_email').value
            const amount = document.querySelector('#payment_amount').value
            const i_date = document.querySelector('#investment_date').value
            const new_currency = document.querySelector('#payment_currency').value
            const new_date = new Date(i_date)
            returns = amount * percentage
            $.ajax({
                    url: 'invest',
                    dataType: "JSON",
                    beforeSend: () => {
                        $('.main_form').fadeOut()
                        $('#id01').fadeIn()

                    },
                    data: {
                        "email": email,
                        "amount": amount,
                        "currency": new_currency,
                        "returns": parseFloat(amount) + parseFloat(returns),
                        "Duration": 7,
                        "plan": currentPlan,
                        "percent": percentage,
                        "User_date": {
                            "day": new_date.getDate(),
                            "month": parseInt(new_date.getMonth()),
                            "Year": new_date.getFullYear()
                        }
                    },
                    type: "POST",
                    success: (result) => {
                        if (result.Success == true) {
                            $('#id01').fadeOut()
                            $('.crypto_details').fadeIn()
                        } else {
                            alert('An Error Occurred ')
                        }
                    },
                })
                // let setup = PaystackPop.setup({
                //     key: public_key, // Replace with your public key
                //     email,
                //     amount, // the amount value is multiplied by 100 to convert to the lowest currency unit
                //     currency: 'NGN',
                //     callback: function(response) {
                //         console.log(returns)
                //         console.log(amount)
                //         $.ajax({
                //                 url: 'invest',
                //                 dataType: "JSON",
                //                 data: {
                //                     "email": email,
                //                     "amount": amount,
                //                     "currency": new_currency,
                //                     "returns": amount + returns,
                //                     "Duration": 70,
                //                     "plan": currentPlan
                //                 },
                //                 type: "POST",
                //                 success: (result) => {
                //                     console.log(result)
                //                 },
                //             })
                //             //this happens after the payment is completed successfully
                //             // var reference = response.reference;
                //             // alert('Payment complete! Reference: ' + reference);
                //             // Make an AJAX call to your server with the reference to verify the transaction
                //     },
                //     onClose: function() {

            //     },
            // });
            // setup.openIframe();
        }
    })
    $('#edit-account').click(() => {
        $('#update_account').slideToggle()
    })

    $('.btc-form').submit(() => {
        event.preventDefault()
        var btc_wallet = document.querySelector('#btc-input').value
        $.ajax({
            url: "addWallet",
            beforeSend: () => {
                $('#btc-send').fadeOut()
                $('#btc-spinner').fadeIn()

            },
            data: {
                "wallet_id": btc_wallet,
                "wallet_type": "BTC"
            },
            dataType: "JSON",
            type: "POST",
            success: (data) => {
                var new_data = data
                if (new_data.Status == "Success") {
                    $('#btc-spinner').fadeOut()
                    $('.btc-db-check').fadeIn()
                    setTimeout(() => {
                        $('.btc-db-check').fadeOut()
                        $('#btc-send').fadeIn()
                    }, 6000)
                } else {
                    $('#btc-spinner').fadeOut()
                    $('#btc-err').fadeIn()
                    setTimeout(() => {
                        $('#btc-err').fadeOut()
                        $('#btc-send').fadeIn()
                    }, 3000)
                }
            },
            error: (err) => {
                console.log(err)
            }

        })
    })
    $('.eth-form').submit(() => {
        event.preventDefault()
        var eth_wallet = document.querySelector('#ether-input').value
        $.ajax({
            url: "addWallet",
            beforeSend: () => {
                $('#eth-send').fadeOut()
                $('#eth-spinner').fadeIn()
            },
            data: {
                "wallet_id": eth_wallet,
                "wallet_type": "ETHERUM"
            },
            dataType: "JSON",
            type: "POST",
            success: (data) => {
                var new_data = data
                if (new_data.Status == "Success") {
                    $('#eth-spinner').fadeOut()
                    $('.eth-db-check').fadeIn()
                    setTimeout(() => {
                        $('.eth-db-check').fadeOut()
                        $('#eth-send').fadeIn()
                    }, 3000)
                } else {
                    $('.eth-spinner').fadeOut()
                    $('#eth-err').fadeIn()
                    setTimeout(() => {
                        $('#eth-err').fadeOut()
                        $('#eth-send').fadeIn()
                    }, 3000)
                }

            },
            error: (err) => {
                console.log(err)
            }

        })
    })

})