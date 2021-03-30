  $(document).ready(() => {
      const functions = {
          new_admin_email: (val, id) => {

          },
          new_admin_name: (val, id) => {
              const err_tag = document.querySelector(`#${id}_err`)
              const regex = /[0-9]+/i
              if (regex.exec(val)) {
                  let error_text = "Only Letters are Allowed"
                  err_code = error_text
                  all_errors[id] = err_code
                  err_tag.innerHTML = err_code
              } else {
                  err_code = ""
                  all_errors[id] = err_code
                  err_tag.innerHTML = err_code
              }
          },
          new_admin_username: (val, id) => {
              const err_tag = document.querySelector(`#${id}_err`)
              const regex = /^[a-z|0-9|@|_]+/i
              if (regex.exec(val)) {
                  err_code = ""
                  all_errors[id] = err_code
                  err_tag.innerHTML = err_code
                  if (val.includes(' ')) {
                      let error_text = "Username Can Contain Only aphabets And Some special characters like @ and _"
                      all_errors[id] = error_text
                      err_code = error_text
                      err_tag.innerHTML = err_code
                  } else {
                      err_code = ""
                      all_errors[id] = err_code
                      err_tag.innerHTML = err_code
                  }
              } else {
                  let error_text = "Username Can Contain Only aphabets And Some special characters like @ and _"
                  err_code = error_text
                  all_errors[id] = err_code
                  err_tag.innerHTML = err_code

              }
          },
          new_admin_password: (val, id) => {
              const err_tag = document.querySelector(`#${id}_err`)
              const regex = /[a-z]+/i
              const regex2 = /[0-9]+/i
              if (regex.exec(val) && regex2.exec(val)) {

                  if (val.includes(' ')) {
                      let error_text = "Password cannot Contain WhiteSpace"
                      all_errors[id] = error_text
                      err_code = error_text
                      err_tag.innerHTML = err_code
                  } else {
                      err_code = ""
                      all_errors[id] = err_code
                      err_tag.innerHTML = err_code
                  }

              } else {
                  let error_text = "Password must Contain atleast A number and alphabets"
                  all_errors[id] = error_text
                  err_code = error_text
                  err_tag.innerHTML = err_code
              }
          },
          new_admin_confirm_password: (val, id) => {
              const err_tag = document.querySelector(`#${id}_err`)
              const password = document.querySelector('#new_admin_password').value
              if (password == val) {
                  err_code = ""
                  all_errors[id] = err_code
                  err_tag.innerHTML = err_code
              } else {
                  let error_text = "Passwords Do Not match"
                  err_code = error_text
                  all_errors[id] = err_code
                  err_tag.innerHTML = err_code
              }
          }
      }
      let err_code = ""
      const all_errors = {
          new_admin_name: "",
          new_admin_username: "",
          new_admin_password: "",
          new_admin_confirm_password: ""
      }

      $('#addAdminBtn').click(() => {
              $('#addAdmin').slideToggle()
          }),
          $('#add_promo_btn').click(() => {
              $('#new_promo').fadeToggle()
          }),

          deleteAdmin = (id) => {
              if (confirm("Are You Sure You Want To Delete This Admin?")) {
                  $.ajax({
                      type: "POST",
                      url: "deleteAdmin",
                      data: {
                          "id": id
                      },
                      dataType: 'JSON',
                      beforeSend: () => {
                          $(`#loader_${id}`).fadeIn()
                      },
                      complete: () => {
                          $(`#loader_${id}`).fadeOut()

                      },
                      success: (data) => {
                          if (data.Success == "True") {
                              alert('Admin Deleted')
                              location.reload()
                          } else {
                              alert('An Error Occured')
                          }
                      }

                  })
              }
          }
      acceptWithdrawal = (id, email, date, amount) => {
          if (confirm("Do You Want To Accept?")) {
              $.ajax({
                  type: "POST",
                  url: "accept",
                  data: {
                      "id": id,
                      "email": email,
                      "date": date,
                      "amount": amount

                  },
                  dataType: 'JSON',
                  success: (data) => {
                      if (data.Success) {
                          location.reload()
                      }
                  }

              })
          } else {

          }

      }
      rejectWithdrawal = (id, email, date, amount) => {
          if (confirm("Are You Sure You Want To Reject?")) {
              $.ajax({
                  type: "POST",
                  url: "reject",
                  data: {
                      "id": id,
                      "email": email,
                      "date": date,
                      "amount": amount

                  },
                  dataType: 'JSON',
                  success: (data) => {
                      if (data.Success) {
                          location.reload()
                      }
                  }

              })
          } else {

          }

      }
      suspendAdmin = (id) => {
          if (confirm("Are You sure You Want To Suspend This Admin")) {
              $.ajax({
                  type: "POST",
                  url: "suspendAdmin",
                  data: {
                      "id": id
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#loader_${id}`).fadeIn()
                  },
                  complete: () => {
                      $(`#loader_${id}`).fadeOut()
                  },
                  success: (data) => {
                      if (data.Success == "True") {
                          alert('Admin Suspended')
                          location.reload()
                      } else {
                          alert('An Error Occured')
                      }
                  }


              })
          } else {

          }
      }
      Resume = (id) => {
          if (confirm("Are You sure You Want To Resume This Admin")) {
              $.ajax({
                  type: "POST",
                  url: "ResumeAdmin",
                  data: {
                      "id": id
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#loader_${id}`).fadeIn()
                  },
                  complete: () => {
                      $(`#loader_${id}`).fadeOut()
                  },
                  success: (data) => {
                      if (data.Success == "True") {
                          alert('Admin Resumed')
                          location.reload()
                      } else {
                          alert('An Error Occured')
                      }
                  }


              })
          } else {

          }
      }
      ResumePromo = (id) => {
          if (confirm("Are You sure You Want To Resume This Promo")) {
              $.ajax({
                  type: "POST",
                  url: "resumePromo",
                  data: {
                      "id": id
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#loader_${id}`).fadeIn()
                  },
                  complete: () => {
                      $(`#loader_${id}`).fadeOut()
                  },
                  success: (data) => {
                      if (data.Success == "True") {
                          alert('Promo Resumed')
                          location.reload()
                      } else {
                          alert('An Error Occured')
                      }
                  }


              })
          } else {

          }
      }
      deletePromo = (id) => {
          $.ajax({
              type: "POST",
              url: "deletePromo",
              data: {
                  "id": id
              },
              dataType: 'JSON',
              beforeSend: () => {
                  $(`#loader_${id}`).fadeIn()
              },
              complete: () => {
                  $(`#loader_${id}`).fadeOut()
              },
              success: (data) => {
                  if (data.Success == "True") {
                      alert('Promo Deleted')
                      location.reload()
                  } else {
                      alert('An Error Occured')
                  }
              }

          })
      }
      suspendPromo = (id) => {
          if (confirm("Are You sure You Want To Suspend This Promo")) {
              $.ajax({
                  type: "POST",
                  url: "suspendPromo",
                  data: {
                      "id": id
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#loader_${id}`).fadeIn()
                  },
                  complete: () => {
                      $(`#loader_${id}`).fadeOut()
                  },
                  success: (data) => {
                      if (data.Success == "True") {
                          alert('Promo Suspended')
                          location.reload()
                      } else {
                          alert('An Error Occured')
                      }
                  }


              })
          } else {

          }
      }
      endPromo = (id) => {
          if (confirm("Are You sure You Want To End This Promo")) {
              $.ajax({
                  type: "POST",
                  url: "endPromo",
                  data: {
                      "id": id
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#loader_${id}`).fadeIn()
                  },
                  complete: () => {
                      $(`#loader_${id}`).fadeOut()
                  },
                  success: (data) => {
                      if (data.Success == "True") {
                          alert('Promo Ended')
                          location.reload()
                      } else {
                          alert('An Error Occured')
                      }
                  }


              })
          } else {

          }
      }
      resumePromo = (id) => {
          if (confirm("Are You sure You Want To Resume This Promo")) {
              $.ajax({
                  type: "POST",
                  url: "resumePromo",
                  data: {
                      "id": id
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#loader_${id}`).fadeIn()
                  },
                  complete: () => {
                      $(`#loader_${id}`).fadeOut()
                  },
                  success: (data) => {
                      if (data.Success == "True") {
                          alert('Promo Resumed')
                          location.reload()
                      } else {
                          alert('An Error Occured')
                      }
                  }


              })
          } else {

          }
      }
      registerAdmin = (name, email, password, username) => {

              $.ajax({
                  type: "POST",
                  url: "addAdmin",
                  data: {
                      name,
                      email,
                      password,
                      username
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#admin_form_loader`).fadeIn()
                  },
                  complete: () => {
                      $(`#admin_form_loader`).fadeOut()
                  },
                  success: (data) => {
                      console.log(data)
                      if (data.Success == "True") {
                          document.querySelector('#err_messages').innerHTML = `
                            <h4 class="w3-text-green w3-pale-green p-3">${data.Error}</h4>
                            `
                          location.reload()
                      } else {
                          document.querySelector('#err_messages').innerHTML = `
                            <h4 class="w3-text-red w3-pale-red p-3">${data.Error}</h4>
                            `
                          $('#err_messages').fadeIn()
                      }
                  }


              })

          },
          addPromo = (title, duration, description) => {

              $.ajax({
                  type: "POST",
                  url: "promo",
                  data: {
                      title,
                      duration,
                      description
                  },
                  dataType: 'JSON',
                  beforeSend: () => {
                      $(`#admin_form_loader`).fadeIn()
                  },
                  complete: () => {
                      $(`#admin_form_loader`).fadeOut()
                  },
                  success: (data) => {
                      if (data.Success == "True") {
                          alert('Promo Added')
                          location.reload()
                      } else {
                          alert(data.error)
                      }
                  }


              })

          },

          $('#add_admin_form').submit(() => {
              event.preventDefault()
              const name = document.getElementById('new_admin_name').value
              const email = document.getElementById('new_admin_email').value
              const password = document.getElementById('new_admin_password').value
              const username = document.getElementById('new_admin_username').value
              let {
                  new_admin_name,
                  new_admin_username,
                  new_admin_password,
                  new_admin_confirm_password
              } = all_errors
              const err_arrays = [new_admin_name, new_admin_username, new_admin_password, new_admin_confirm_password]
              const new_array = err_arrays.filter(arr => {
                  if (arr != "") {
                      return arr
                  }
              })
              if (new_array.length > 0) {
                  let elements = ""
                  new_array.forEach(w => {
                      elements += `
                         <h4.w3-text-red>${w}</h4></br>
                        `
                  })
                  document.querySelector('#err_messages').innerHTML = `
                    <div class="w3-pale-red w3-text-red">
                        ${elements}
                    </div>
                    `
                  $('#err_messages').fadeIn()
              } else {
                  registerAdmin(name, email, password, username)
              }

              // console.log(name, email, password, username)
              // $.ajax({
              //     type: "POST",
              //     url: "addAdmin",
              //     data: {
              //         name,
              //         email,
              //         password,
              //         username
              //     },
              //     dataType: 'JSON',
              //     beforeSend: () => {
              //         $(`#admin_form_loader`).fadeIn()
              //     },
              //     complete: () => {
              //         $(`#admin_form_loader`).fadeOut()
              //     },
              //     success: (data) => {
              //         console.log(data)
              //     }


              // })
          })
      $('#new_promo_form').submit(() => {
          event.preventDefault()
          const title = document.getElementById('promo_title').value
          const duration = document.getElementById('promo_duration').value
          const description = document.getElementById('promo_description').value
          let {
              new_admin_name,
              new_admin_username,
              new_admin_password,
              new_admin_confirm_password
          } = all_errors
          const err_arrays = [new_admin_name, new_admin_username, new_admin_password, new_admin_confirm_password]
          addPromo(title, duration, description)
              // console.log(name, email, password, username)
              // $.ajax({
              //     type: "POST",
              //     url: "addAdmin",
              //     data: {
              //         name,
              //         email,
              //         password,
              //         username
              //     },
              //     dataType: 'JSON',
              //     beforeSend: () => {
              //         $(`#admin_form_loader`).fadeIn()
              //     },
              //     complete: () => {
              //         $(`#admin_form_loader`).fadeOut()
              //     },
              //     success: (data) => {
              //         console.log(data)
              //     }


          // })
      })
      if (location.pathname == "/admin/admins") {
          const admin = document.querySelectorAll('.admin-input')
          admin.forEach((input) => {
              input.addEventListener('input', (e) => {
                  const target = e.target
                  const val = target.value
                  const f_id = target.id

                  functions[f_id](val, f_id)
              })
          })
      }
  })