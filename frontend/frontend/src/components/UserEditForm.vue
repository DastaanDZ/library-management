<template>
  <div class="registration-form">
    <h1>EDIT PROFILE</h1>
    <form @submit.prevent="saveChanges">
      <div class="form-group text-start mb-1">
        <label for="username">Username:</label>
        <input
          v-model="userData.username"
          type="text"
          class="form-control item"
          id="username"
          placeholder="Username"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="password">Password:</label>
        <input
          v-model="userData.password"
          type="password"
          class="form-control item"
          id="password"
          placeholder="Password"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="email">Email:</label>
        <input
          v-model="userData.email"
          type="text"
          class="form-control item"
          id="email"
          placeholder="Email"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="role">Role:</label>
        <input
          v-model="userData.role"
          type="text"
          class="form-control item"
          id="role"
          placeholder="Role"
        />
      </div>
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-block create-account">
          Save Changes
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "UserEditForm",
  data() {
    return {
      userData: {
        username: "",
        password: "",
        email: "",
        role: "",
      },
    };
  },
  methods: {
    async saveChanges() {
      try {
        // Retrieve access token from localStorage
        const accessToken = localStorage.getItem("accessToken");

        if (!accessToken) {
          throw new Error("Access token not found");
        }

        // Decode the access token to extract user ID
        const decodedToken = jwtDecode(accessToken);
        console.log(decodedToken);
        const userId = decodedToken.sub;

        // Check if user ID is valid
        if (!userId) {
          throw new Error("Invalid user ID");
        }

        // Make PUT request to update user data
        const response = await axios.put(
          `http://127.0.0.1:5000/edit-user/${userId}`,
          this.userData
        );
        console.log(response.data);
        // Optionally, you can show a success message or redirect the user after successful update
      } catch (error) {
        console.error("Error updating user:", error);
        // Handle error - e.g., show an error message to the user
        if (error.response && error.response.status === 401) {
          // Unauthorized access, redirect to login page
          this.$router.push("/login");
        } else {
          // Other errors, redirect to user info page
          this.$router.push("/user-info");
        }
      }
    },
  },
};
</script>

<style>
body {
  /* background-color: #dee9ff; */
}

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

.registration-form .create-account {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: bold;
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
