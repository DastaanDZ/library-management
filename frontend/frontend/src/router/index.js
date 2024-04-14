import Vue from "vue";
import VueRouter from "vue-router";

import LoginForm from "@/components/LoginForm.vue";
import RegisterForm from "@/components/RegisterForm.vue";
import UserEditForm from "@/components/UserEditForm.vue";
import UserInfo from "@/components/UserInfo.vue";
import MonitorTable from "@/components/MonitorTable.vue";
import CardDetails from "@/components/CardDetails.vue";
import UserDetail from "@/components/UserDetail.vue";

import Issued from "@/views/Issued.vue";
import Requested from "@/views/requested.vue";
import LandingPage from "@/views/LandingPage.vue";
import Librarian from "@/views/Librarian.vue";
import LibCardDetails from "@/components/LibCardDetails.vue";
import Feedback from "@/views/Feedback.vue";
import AddBook from "@/views/AddBook.vue";
import AssignSection from "@/views/AssignSection.vue";
import AddSection from "@/views/AddSection.vue";
import EditBook from "@/views/EditBook.vue";
import Home from "@/views/Home.vue";
import ViewAll from "@/views/ViewAll.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/user",
    name: "LandingPage",
    component: LandingPage,
    props: { roleRequired: "user" },
  },
  {
    path: "/librarian",
    name: "Librarian",
    component: Librarian,
    props: { roleRequired: "librarian" },
  },
  {
    path: "/userdetail",
    name: "UserDetail",
    component: UserDetail,
  },
  {
    path: "/card-details/:book_id",
    name: "CardDetails",
    component: CardDetails,
    props: true,
  },
  {
    path: "/lib-card-details/:book_id",
    name: "LibCardDetails",
    component: LibCardDetails,
    props: true,
  },
  {
    path: "/register",
    name: "RegisterForm",
    component: RegisterForm,
  },
  {
    path: "/login",
    name: "LoginForm",
    component: LoginForm,
  },
  {
    path: "/user-info",
    name: "UserInfo",
    component: UserInfo,
  },
  {
    path: "/user-edit/:user_id",
    name: "UserEditForm",
    component: UserEditForm,
  },
  {
    path: "/add-book",
    name: "AddBookForm",
    component: AddBook,
  },
  {
    path: "/edit-book/:book_id",
    name: "EditBook",
    component: EditBook,
    props: true,
  },
  {
    path: "/monitor",
    name: "MonitorTable",
    component: MonitorTable,
  },
  {
    path: "/view-all",
    name: "ViewAll",
    component: ViewAll,
    props: true,
  },
  {
    path: "/requested",
    name: "Requested",
    component: Requested,
    props: { heading: "REQUESTED" },
  },
  {
    path: "/issued",
    name: "Issued",
    component: Issued,
    props: { heading: "ISSUED" },
  },
  {
    path: "/issued",
    name: "Issued",
    component: Issued,
    props: { heading: "ISSUED" },
  },
  {
    path: "/feedback/:book_id",
    name: "FeedbackForm",
    component: Feedback,
  },
  {
    path: "/assign-section",
    name: "AssignSection",
    component: AssignSection,
  },
  {
    path: "/add-section",
    name: "AddSection",
    component: AddSection,
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
