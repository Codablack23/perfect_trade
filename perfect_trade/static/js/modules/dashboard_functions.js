export const public_key = 'pk_test_a6808fe6b78ec1ff545c54baaaa6ba990d7bc60d'
export const api_key = '22e8c7fda4cc950b8a9f'

export const loadbalance = () => {
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
export const loadInvestments = () => {
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
export const loadAccount = () => {
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
export const loadRequestedWithdraws = () => {
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
export const sendWithdraws = () => {
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
export const updateAccount = () => {
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