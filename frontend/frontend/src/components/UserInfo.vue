<template>
  <section style="background-color: #eee">
    <div class="container py-5">
      <div class="row">
        <div class="col-lg-8 offset-lg-2">
          <div class="card">
            <div class="card-body">
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Username:</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{ userData.username }}</p>
                </div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Email:</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{ userData.email }}</p>
                </div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Role:</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{ userData.role }}</p>
                </div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">No. of Books Issued:</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{ booksIssued }}</p>
                </div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">No. of Books Requested:</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{ booksRequested }}</p>
                </div>
              </div>
            </div>
          </div>
          <router-link
            :to="{ name: 'UserEditForm', params: { userId: userData.id } }"
          >
            <button type="button" class="btn btn-primary m-2">Edit</button>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "UserInfo",
  data() {
    return {
      userData: {},
      booksIssued: 0,
      booksRequested: 0,
    };
  },
  mounted() {
    this.fetchUserInfo();
    this.fetchBooksIssued();
    this.fetchBooksRequested();
  },
  methods: {
    async fetchUserInfo() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/user-info/${this.$route.params.userId}`
        );
        this.userData = response.data;
      } catch (error) {
        console.error("Error fetching user info:", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    async fetchBooksIssued() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/books-issued/${this.$route.params.userId}`
        );
        this.booksIssued = response.data.count;
      } catch (error) {
        console.error("Error fetching books issued:", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    async fetchBooksRequested() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/books-requested/${this.$route.params.userId}`
        );
        this.booksRequested = response.data.count;
      } catch (error) {
        console.error("Error fetching books requested:", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }
    },
  },
};
</script>
