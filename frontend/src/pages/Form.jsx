import { useState, useEffect } from "react"
import axios from "axios"


export const Form = () => {
  const [testingData, setTestingData] = useState([])

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  useEffect(() => {
    axios
      .get('http://localhost:8000/api/', {
        params: { pk: "abc" },
      })
      .then((response) => response)
      .then((data) => {
        setTestingData(data['data']['test'])
      })
      .catch((err) => {
        console.log(err.message)
      })
  }, [])

  function submit(event) {
    // axios.post(
    //   'http://localhost:8000/post/', 
    //   JSON.stringify({"aaa": "bbb"}), 
    //   {
    //     headers: {
    //       "Content-Type": "application/json",
    //       "X-CSRFToken": getCookie('csrftoken'),
    //     },
    //     credentials: "include",
    //   }
    // )
    // .then((response) => console.log(response))
    // .catch((err) => console.log(err))

    fetch("http://localhost:8000/post/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie('csrftoken')
      },
      credentials: "include",
      body: JSON.stringify({"aaa": "bbb"}),
    })
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.log(err);
    });
  }

  return (
    <div class="otree-body container">
      <button type="submit" className="FooterRegisterForm__registerButton" onClick={submit}>submit</button>
      <h2 class="otree-title page-header">Survey</h2>
      <form
        class="otree-form"
        method="post"
        id="form"
        autocomplete="off"
      >
        <input
          type="hidden"
          name="csrfmiddlewaretoken"
          value="XrBNGM0QHb1P0dLEcfI6CvA1kS0W00m4lCGX2TyZ5pw9QgVqQmVUh67lbtpEdcLs"
        />
        <div class="_otree-content">
          <p>Please answer the following questions.</p>

          <p>{testingData}</p>

          <div class="form-group required">
            <label class="col-form-label" for="id_age">
              What is your age?
            </label>
            <div class="controls  field-age">
              <input
                type="number"
                name="age"
                min="13"
                max="125"
                required
                id="id_age"
                class="form-control"
              />
            </div>
          </div>
          <p>
            <button class="otree-btn-next btn btn-primary">Next</button>
          </p>
        </div>
      </form>
    </div>
  )
}