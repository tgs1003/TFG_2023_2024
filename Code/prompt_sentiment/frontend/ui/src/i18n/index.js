import Vue from "vue";
import { I18n } from "translated";
import VueTranslated from "vue-translated";
import TokenService from "../services/token.service";

Vue.use(VueTranslated);

const locale = TokenService.getlocale(); // replace this with `process.env.LOCALE` or similar
const messages = require(`./messages/${locale}`).default;
const formats = require(`./formats/${locale}`).default;

export default new I18n({ locale, messages, formats });
