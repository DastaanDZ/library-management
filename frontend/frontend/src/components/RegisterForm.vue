<template>
  <div class="vue-tempalte">
    <Navbar />
    <form @submit.prevent="submitForm">
      <h3>Sign Up</h3>
      <div class="mb-3">
        <label>Full Name</label>
        <input
          v-model.trim="fullName"
          type="text"
          class="form-control form-control-lg"
          :class="{ 'is-invalid': errors.fullName }"
        />
        <div class="invalid-feedback" v-if="errors.fullName">
          {{ errors.fullName }}
        </div>
      </div>
      <div class="mb-3">
        <label>Email address</label>
        <input
          v-model.trim="email"
          type="email"
          class="form-control form-control-lg"
          :class="{ 'is-invalid': errors.email }"
        />
        <div class="invalid-feedback" v-if="errors.email">
          {{ errors.email }}
        </div>
      </div>
      <div class="mb-3">
        <label>Password</label>
        <input
          v-model.trim="password"
          type="password"
          class="form-control form-control-lg"
          :class="{ 'is-invalid': errors.password }"
        />
        <div class="invalid-feedback" v-if="errors.password">
          {{ errors.password }}
        </div>
      </div>
      <button type="submit" class="btn btn-dark btn-lg btn-block">
        Sign Up
      </button>
      <p class="forgot-password text-right">
        Already registered
        <router-link :to="{ name: 'login' }">sign in?</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "./Navbar.vue";

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      fullName: "",
      email: "",
      password: "",
      errors: {}, // Object to store form validation errors
    };
  },
  methods: {
    submitForm() {
      // Clear previous errors
      this.errors = {};

      // Perform form validation
      if (!this.fullName) {
        this.errors.fullName = "Full Name is required";
      }
      if (!this.email) {
        this.errors.email = "Email is required";
      } else if (!this.isValidEmail(this.email)) {
        this.errors.email = "Invalid email format";
      }
      if (!this.password) {
        this.errors.password = "Password is required";
      }

      // If there are validation errors, prevent form submission
      if (Object.keys(this.errors).length > 0) {
        return;
      }

      // Prepare the form data object
      const formData = {
        username: this.fullName,
        email: this.email,
        password: this.password,
      };

      // Make an HTTP POST request to the backend route
      const path = "http://127.0.0.1:5000/register";
      axios
        .post(path, formData)
        .then((response) => {
          console.log(response.data.message); // Log the response message
          // Optionally, you can redirect the user or show a success message here
        })
        .catch((error) => {
          console.error("Error:", error); // Log any errors
          // Optionally, you can display an error message to the user
        });
    },
    isValidEmail(email) {
      // Regular expression to validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
  },
};
</script>
