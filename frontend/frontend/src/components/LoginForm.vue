<template>
  <div class="registration-form">
    <h1>Login</h1>
    <form @submit.prevent="loginUser">
      <div class="form-group text-start mb-1">
        <label for="username">Username:</label>
        <input
          v-model="username"
          type="text"
          class="form-control item"
          id="username"
          placeholder="Username"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="password">Password:</label>
        <input
          v-model="password"
          type="password"
          class="form-control item"
          id="password"
          placeholder="Password"
        />
      </div>
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-block create-account">
          Login
        </button>
        <router-link :to="{ path: '/register' }">
          <button
            type="button"
            class="btn btn-block create-account"
            style="margin-left: 1rem"
          >
            Register
          </button>
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    loginUser() {
      const formData = {
        username: this.username,
        password: this.password,
      };

      const path = "http://127.0.0.1:5000/login";
      axios
        .post(path, formData)
        .then((response) => {
          if (
            response.data &&
            response.data.access_token &&
            response.data.role
          ) {
            localStorage.setItem("accessToken", response.data.access_token);
            localStorage.setItem("role", response.data.role);
            console.log("token set in local storage");
            if (response.data.role == "user") {
              console.log("Redirecting to user");
              this.$router.push("/user");
            } else if (response.data.role == "librarian") {
              console.log("Redirecting to librarian");
              this.$router.push("/librarian");
            } else {
              this.$router.push("/");
            }
          } else {
            console.error("Access token not found in response data");
            alert("Invalid response from the server. Please try again.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          if (error.response && error.response.status === 401) {
            this.$router.push("/login");
          } else {
            alert("Invalid username or password. Please try again.");
          }
        });
    },
  },
};
</script>

<style>
.registration-form {
  padding: 50px 0;
}

.registration-form form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.registration-form .form-icon {
  text-align: center;
  background-color: #5891ff;
  border-radius: 50%;
  font-size: 40px;
  color: white;
  width: 100px;
  height: 100px;
  margin: auto;
  margin-bottom: 50px;
  line-height: 100px;
}

.registration-form .item {
  border-radius: 20px;
  margin-bottom: 25px;
  padding: 10px 20px;
}

.registration-form .create-account .register-account {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  background-color: #5791ff;
  border: none;
  color: white;
  margin-top: 20px;
}

.registration-form .social-media {
  max-width: 600px;
  background-color: #fff;
  margin: auto;
  padding: 35px 0;
  text-align: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
  color: #9fadca;
  border-top: 1px solid #dee9ff;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.registration-form .social-icons {
  margin-top: 30px;
  margin-bottom: 16px;
}

.registration-form .social-icons a {
  font-size: 23px;
  margin: 0 3px;
  color: #5691ff;
  border: 1px solid;
  border-radius: 50%;
  width: 45px;
  display: inline-block;
  height: 45px;
  text-align: center;
  background-color: #fff;
  line-height: 45px;
}

.registration-form .social-icons a:hover {
  text-decoration: none;
  opacity: 0.6;
}

@media (max-width: 576px) {
  .registration-form form {
    padding: 50px 20px;
  }

  .registration-form .form-icon {
    width: 70px;
    height: 70px;
    font-size: 30px;
    line-height: 70px;
  }
}
</style>
