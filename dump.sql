--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

\connect itucsdb

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: banner; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY banner (banner_id, link_address, image_url, title) FROM stdin;
1	asdsa	qewqas	asdsaqw
\.


--
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY event (event_id, event_date, tournament_id, place_id) FROM stdin;
\.


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY team (team_id, team_name, team_player_count, event_id) FROM stdin;
\.


--
-- Data for Name: tournament; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY tournament (tournament_id, tournament_name, tournament_type, tournament_date, tournament_length) FROM stdin;
1	tour de france	type1	2015-12-25	50
\.


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

