<template>
  <div class="feedback-form">
    <h1>FEEDBACK</h1>
    <form @submit.prevent="submitFeedback">
      <div class="form-group text-start mb-1">
        <label for="feedback">Feedback:</label>
        <textarea
          v-model="feedbackData.feedback_text"
          class="form-control item"
          id="feedback"
          rows="5"
          placeholder="Write your feedback here..."
        ></textarea>
      </div>
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-block create-account">
          Submit Feedback
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "FeedbackForm",
  data() {
    return {
      feedbackData: {
        feedback_text: "",
      },
    };
  },
  methods: {
    async submitFeedback() {
      try {
        const accessToken = localStorage.getItem("accessToken");

        await axios.post(
          `http://127.0.0.1:5000/feedback/${this.$route.params.book_id}`,
          this.feedbackData,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        alert("Feedback submitted successfully");
        console.log("Feedback submitted successfully");
        // Redirect the user to another page after feedback submission if needed
        this.$router.push(`/user`);
      } catch (error) {
        console.error("Error submitting feedback:", error);
      }
    },
  },
};
</script>

<style>
.feedback-form {
  padding: 50px 0;
}

.feedback-form form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.feedback-form .form-group {
  margin-bottom: 20px;
}

.feedback-form .item {
  border-radius: 20px;
  padding: 10px 20px;
}

.feedback-form .create-account {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: bold;
  background-color: #5791ff;
  border: none;
  color: white;
  margin-top: 20px;
}

@media (max-width: 576px) {
  .feedback-form form {
    padding: 50px 20px;
  }
}
</style>
