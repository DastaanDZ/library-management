<template>
  <div class="main">
    <div class="user-div">
      <div class="dp">
        <img src="cover.png" alt="" />
      </div>
      <h3>Hello, {{ username }}</h3>
    </div>
    <router-link
      :to="{ name: 'UserInfo', params: { userId: userId } }"
      class="btn btn-primary"
    >
      Edit Personal<br />Details
    </router-link>
    <button @click="logoutUser" class="btn btn-danger">Logout</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserDetail",
  props: {
    username: {
      type: String,
      required: true,
    },
    userId: {
      type: String,
      required: true,
    },
  },
  methods: {
    logoutUser() {
      const accessToken = localStorage.getItem("accessToken");

      const path = "http://127.0.0.1:5000/logout";
      axios
        .post(path, null, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          localStorage.removeItem("accessToken");
          localStorage.removeItem("role");
          console.log("Logout successful");
          this.$router.push("/login");
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
  },
};
</script>

<style scoped>
.main {
  display: flex;
  align-items: center;
  padding: 0 2rem;
  justify-content: space-between;
  background: white;
  border-radius: 2rem;
}
.edit {
  width: 10rem;
  height: 10rem;
  display: flex;
  align-items: end;
  justify-content: center;
  padding: 1rem;
}
.user-div {
  display: flex;
  gap: 2rem;
  padding: 2rem 2rem;
  width: 40rem;
  align-items: center;
}
.dp {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
  border: 2px solid black;
  overflow: hidden;
}
.dp img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}
</style>
