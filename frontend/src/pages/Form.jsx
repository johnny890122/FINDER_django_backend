export const Form = ({ testingData }) => {
  return (
    <div class="otree-body container">
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