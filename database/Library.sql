--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.3

-- Started on 2024-06-10 20:02:29

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: library_pcou_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO library_pcou_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16578)
-- Name: books; Type: TABLE; Schema: public; Owner: library_pcou_user
--

CREATE TABLE public.books (
    id integer NOT NULL,
    title text NOT NULL,
    author text NOT NULL,
    genre text NOT NULL,
    year text NOT NULL,
    stock integer NOT NULL,
    available integer NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.books OWNER TO library_pcou_user;

--
-- TOC entry 220 (class 1259 OID 16577)
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: library_pcou_user
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.books_id_seq OWNER TO library_pcou_user;

--
-- TOC entry 3397 (class 0 OID 0)
-- Dependencies: 220
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: library_pcou_user
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- TOC entry 217 (class 1259 OID 16529)
-- Name: members; Type: TABLE; Schema: public; Owner: library_pcou_user
--

CREATE TABLE public.members (
    member_id integer NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    address text NOT NULL,
    phone character varying(20) NOT NULL,
    borrowed integer NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.members OWNER TO library_pcou_user;

--
-- TOC entry 216 (class 1259 OID 16528)
-- Name: members_member_id_seq; Type: SEQUENCE; Schema: public; Owner: library_pcou_user
--

CREATE SEQUENCE public.members_member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.members_member_id_seq OWNER TO library_pcou_user;

--
-- TOC entry 3398 (class 0 OID 0)
-- Dependencies: 216
-- Name: members_member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: library_pcou_user
--

ALTER SEQUENCE public.members_member_id_seq OWNED BY public.members.member_id;


--
-- TOC entry 219 (class 1259 OID 16551)
-- Name: staff; Type: TABLE; Schema: public; Owner: library_pcou_user
--

CREATE TABLE public.staff (
    staff_id integer NOT NULL,
    name text NOT NULL,
    username text NOT NULL,
    hash text NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.staff OWNER TO library_pcou_user;

--
-- TOC entry 215 (class 1259 OID 16503)
-- Name: staff_id_seq; Type: SEQUENCE; Schema: public; Owner: library_pcou_user
--

CREATE SEQUENCE public.staff_id_seq
    START WITH 4
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_id_seq OWNER TO library_pcou_user;

--
-- TOC entry 218 (class 1259 OID 16550)
-- Name: staff_staff_id_seq; Type: SEQUENCE; Schema: public; Owner: library_pcou_user
--

CREATE SEQUENCE public.staff_staff_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_staff_id_seq OWNER TO library_pcou_user;

--
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 218
-- Name: staff_staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: library_pcou_user
--

ALTER SEQUENCE public.staff_staff_id_seq OWNED BY public.staff.staff_id;


--
-- TOC entry 222 (class 1259 OID 16588)
-- Name: transactions; Type: TABLE; Schema: public; Owner: library_pcou_user
--

CREATE TABLE public.transactions (
    borrower_id integer NOT NULL,
    book_id integer NOT NULL,
    type text NOT NULL,
    employee_id integer NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.transactions OWNER TO library_pcou_user;

--
-- TOC entry 3228 (class 2604 OID 16613)
-- Name: books id; Type: DEFAULT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- TOC entry 3222 (class 2604 OID 16532)
-- Name: members member_id; Type: DEFAULT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.members ALTER COLUMN member_id SET DEFAULT nextval('public.members_member_id_seq'::regclass);


--
-- TOC entry 3225 (class 2604 OID 16609)
-- Name: staff staff_id; Type: DEFAULT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.staff ALTER COLUMN staff_id SET DEFAULT nextval('public.staff_staff_id_seq'::regclass);


--
-- TOC entry 3390 (class 0 OID 16578)
-- Dependencies: 221
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: library_pcou_user
--

COPY public.books (id, title, author, genre, year, stock, available, "time", deleted) FROM stdin;
1	The Fellowship of the Ring (The Lord of the Rings #1)	J.R.R. Tolkien	Fantasy	1954	3	2	2023-04-11 16:26:11	0
2	The Two Towers (The Lord of the Rings #2)	J.R.R. Tolkien	Fantasy	1954	3	1	2024-04-11 16:27:20	0
4	Gone Girl	Gillian Flynn	Thriller	2012	1	0	2024-04-11 16:31:25	0
6	The Hunger Games (The Hunger Games #1)	Suzanne Collins	Fiction	2008	2	1	2024-04-11 16:34:03	0
7	To Kill a Mockingbird	Harper Lee	Fiction	1960	2	0	2024-04-11 16:34:59	0
8	Where the Sidewalk Ends	Shel Silverstein	Poetry	1974	1	0	2024-04-11 16:36:16	0
9	Fairy Tale	Stephen King	Horror	2022	1	0	2024-04-11 16:38:03	0
10	Pride and Prejudice	Jane Austen	Romance	1813	1	0	2024-04-11 17:25:40	0
11	Dune (Dune #1)	Frank Herbert	Science Fiction	1965	2	1	2024-04-11 17:26:45	0
12	The Diary of a Young Girl	Anne Frank	Biography	1947	1	0	2024-04-11 17:27:48	0
14	The Gifts of Imperfection	Brené Brown	Self-help	2010	1	0	2024-04-11 17:30:23	0
15	Misery	Stephen King	Horror	1987	1	0	2024-04-11 17:31:40	0
16	Cosmos	Carl Sagan	Science	1980	2	1	2024-04-25 10:21:14	0
17	Into the Wild	Jon Krakauer	Travel	1996	1	0	2024-04-25 10:22:27	0
18	Murder on the Orient Express	Agatha Christie	Mystery	1934	3	2	2024-04-25 10:24:46	0
19	Chronicles: Volume One	Bob Dylan	Music	2004	1	1	2024-04-25 10:25:55	0
20	The Blind Side	Michael Lewis	Sports	2006	2	2	2024-04-25 10:27:40	0
22	Post Human 2: NeX GeN	BMTH	Music	2024	2	2	2024-05-27 17:27:40	0
25	Lateralus	Tool	Music	2001	5	3	2024-06-10 13:20:20.382	0
3	The Return of the King (The Lord of the Rings #3)	J.R.R. Tolkien	Fantasy	1955	3	1	2024-04-11 16:29:58	0
21	Post Human: Survival Horror	BMTH	Music	2020	2	1	2024-05-25 16:27:40	0
24	Post Human 3	BMTH	Art	2028	12	12	2024-06-10 12:26:00.302647	1
13	The Secret Garden	Frances Hodgson Burnett	Children	1911	2	1	2024-04-11 17:29:09	0
5	A Short History of Nearly Everything	Bill Bryson	History	2003	4	3	2024-04-11 16:32:34	0
\.


--
-- TOC entry 3386 (class 0 OID 16529)
-- Dependencies: 217
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: library_pcou_user
--

COPY public.members (member_id, name, email, address, phone, borrowed, "time", deleted) FROM stdin;
1	Adele L. Fales	adelefales@jourrapide.com	2079 Farm Meadow Drive Seligman, AZ 86337	 928-858-9304	4	2024-04-11 17:36:26	0
3	Leon Jaksic	leonjaksic@example.us	4465 TecumLane Dry Prong, LA 71423	318-899-6794	0	2024-04-11 17:38:53	0
6	Charles Herbert	charles.herbert@jourrapide.com	1710 Dola Mine Road Durham, NC 27707	919-402-7954	0	2024-04-11 17:41:55	0
7	Hudson Auld	h.auld@teleworm.us	4242 Asylum Avenue Waterbury, CT 06702	203-670-0964	1	2024-04-11 17:43:35	0
8	Lilly Strand	strand20@somemail.com	2233 Lewis Street Chicago, IL 60607	630-943-4539	0	2024-04-11 17:45:05	0
9	Helena Cabova	helenacabova@dayrep.com	2614 Apple Lane Peoria, IL 61614	309-206-0128	0	2024-04-11 17:46:15	0
10	Emile S. Vestergaard	emile.vestergaard@armyspy.com	557 Romines Mill Road Dallas, TX 75247	214-645-7394	2	2024-04-11 17:47:25	0
11	Bruno Cadieux	bruno.cad11@example.com	3368 LateAvenue Durant, OK 74701	580-775-2619	2	2024-04-11 17:49:03	0
12	Chungus	chungchang@something.com	2445 Memory Lane Hickory Hills, IL 60457	815-922-0225	0	2024-04-11 17:50:11	0
13	Jens Wagner	j.wagner@armyspy.com	853 Main Street Lynnwood, WA 98036	425-712-0524	0	2024-04-11 17:51:07	0
14	Vinícius Almeida	vinicius.almeida01@rhyta.com	3468 Cheshire Road Greenwich, CT 06830	203-422-0360	0	2024-04-11 17:52:18	0
15	Kathe Holland	kathejholland@jourrapide.com	825 Grey Fox Farm Road Houston, TX 77053	281-810-4351	3	2024-04-11 17:53:27	0
16	James Soto	jamessoto123@joe.com	4851 Hartway Street Armour, SD 57313	605-724-1895	3	2024-04-11 17:54:36	0
17	Michael Cole	michael.cole@dayrep.com	4080 Jarvisville Road Huntington, NY 11743	516-996-5977	0	2024-04-11 17:55:47	0
18	Zlata Kolar	zlata.kolar@example.us	3859 Johnstown Road Lombard, IL 60148	847-401-2507	2	2024-04-11 17:56:46	0
19	Maryn Hoef	maryn.vdhoef@rhyta.com	3949 Berkshire Circle Knoxville, TN 37920	865-609-8875	1	2024-04-11 17:58:08	0
20	Danilo Ricci	d.ricci100@example.net	2971 Hidden Pond Road Nashville, TN 37211	615-680-3494	0	2024-04-11 17:59:37	0
2	Shawn Parrish	shawnparrish@teleworm.us	2576 Pringle Drive Bridgeview, IL 60455	312-399-4956	2	2024-04-11 17:37:25	0
5	Amy Walker	amywalker123@eg.com	144 Breezewood Court Moundridge, KS 67107	620-453-1811	2	2024-04-11 17:40:59	0
4	Jessika Kuster	jessika1@teleworm.us	2653 Private Lane Tifton, GA 31794	229-386-3242	2	2024-04-11 17:39:49	0
\.


--
-- TOC entry 3388 (class 0 OID 16551)
-- Dependencies: 219
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: library_pcou_user
--

COPY public.staff (staff_id, name, username, hash, "time", deleted) FROM stdin;
2	Dylan B	DyLaN	pbkdf2:sha256:260000$82tgmUV19qxdQPVJ$d792add0851f61f7a258f8209bb475c0915f0f320816d1be08d30078538e940d	2024-04-25 10:11:47	0
3	Ed Jones	jones	pbkdf2:sha256:260000$IzyQfL9akRx5mxnr$75d1d2110f00f289bfba738f7c392c6a24efb5f5662f5d6c15a6df8d0b13b2a7	2024-04-25 10:13:46	0
4	Nikki P	nikki	pbkdf2:sha256:260000$uZDgym2ajrD8e705$3fff843ac53af4aa79385f5c05bd3c6894549e22a03c166a1515878ded916c6a	2024-04-25 10:14:21	0
5	Oli	Olii	scrypt:32768:8:1$HY468phMheywaxD2$f60e1a340d89062ff3034ed9a6f3157b08a8ef421ddaa9a17eb6eda6e1ebbc4e75d06cf1830502f40692b408314515a56cee8c5cd083f758085830e20cee2ec1	2024-06-07 15:38:06.382992	0
7	Allisa	Ali	scrypt:32768:8:1$XA7k7IMUOuHFc8of$2ed54217085955f01c062cc94f0cd4d2120cbd359f2ab892463435795e6116c2991d1c05252031278125e060459f0ef7f694b9c3f97c665652a1d1e6a4f2cd9e	2024-06-07 15:39:57.920574	0
6	Luna	luna	scrypt:32768:8:1$Dap6l11HGZEhMp19$bd282f754aa79c2b60c12188c41bb566288ff2feda8f02d78adeb3211d24ecd9e9348c16a4070c44140bbb81510d0a540c712fd44ecec081a6bb5ef353c1e772	2024-06-07 15:38:27.754179	1
1	Administrator	admin	scrypt:32768:8:1$Xduj5YPKmT6Qxv5a$6164f071e53bdf857f18f61e125f2d213397d337bb8a8ec2d5da42cadc6921aade60b9e10ef00ca63e32cb3b945819d7f90c2c76fc5029362158c0d75dd0bf7f	2024-04-11 15:34:54	0
8	Kelly	kell	scrypt:32768:8:1$MKRkWFTsI3qVeRBa$2def2ab9d4cc44d833759c2072817144668ae240041de58eef276ac462e397136021a87b18952d3823f925954fec0d1584c83a62fa3d516f054bdccb946d8492	2024-06-08 23:49:37.796199	1
9	Paddy	Paddy	scrypt:32768:8:1$yAbpahza9af3va9l$f756ace12588285da80099f81335fb402c7dc264065c6df0d8f5956eea2d3bbc0e8db6db4425966bc6019be3c8fa67cdc592e57f714a196346ef603583e59f00	2024-06-10 16:42:15.187575	1
\.


--
-- TOC entry 3391 (class 0 OID 16588)
-- Dependencies: 222
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: library_pcou_user
--

COPY public.transactions (borrower_id, book_id, type, employee_id, "time") FROM stdin;
10	14	borrowed	1	2024-04-13 10:29:41
2	1	borrowed	1	2024-04-15 10:30:10
2	2	borrowed	1	2024-04-15 10:30:10
2	3	borrowed	1	2024-04-15 10:30:10
19	11	borrowed	2	2024-04-16 10:30:33
15	6	borrow	2	2024-04-25 10:32:12
15	10	borrow	2	2024-04-25 10:32:12
10	14	returned	2	2024-04-25 10:33:07
3	20	borrowed	3	2024-04-25 10:33:30
19	11	returned	3	2024-04-25 10:33:40
18	2	borrow	3	2024-04-25 10:33:58
18	7	borrow	3	2024-04-25 10:33:58
2	1	returned	4	2024-04-25 10:34:18
2	2	returned	4	2024-04-25 10:34:18
2	3	returned	4	2024-04-25 10:34:18
15	11	borrowed	4	2024-04-20 10:34:32
19	8	borrowed	4	2024-04-20 10:35:02
19	19	borrowed	4	2024-04-20 10:35:02
15	11	returned	4	2024-04-25 10:35:49
19	8	returned	1	2024-04-25 10:36:01
19	19	returned	1	2024-04-25 10:36:01
4	15	borrow	1	2024-04-25 10:36:16
4	12	borrowed	1	2024-04-25 10:36:17
3	20	returned	1	2024-04-25 10:36:52
19	1	borrow	1	2024-04-25 10:37:31
10	8	borrow	2	2024-04-25 10:38:14
10	19	borrowed	2	2024-04-25 10:38:14
10	17	borrow	2	2024-04-25 10:38:14
7	4	borrow	2	2024-04-25 10:38:32
4	12	returned	2	2024-04-25 10:38:41
15	12	borrow	3	2024-04-25 10:39:19
11	11	borrow	3	2024-04-25 10:39:40
11	5	borrow	3	2024-04-25 10:39:40
1	7	borrow	4	2024-04-25 10:40:25
1	13	borrow	4	2024-04-25 10:40:25
1	3	borrow	4	2024-04-25 10:40:25
1	2	borrow	4	2024-04-25 10:40:25
16	14	borrow	4	2024-04-25 10:40:55
10	19	returned	4	2024-04-25 10:41:11
5	9	borrow	1	2024-04-25 10:41:37
16	16	borrow	1	2024-04-25 10:42:20
16	18	borrow	1	2024-04-25 10:42:20
2	3	borrow	1	2024-06-07 14:25:54.674532
2	21	borrow	1	2024-06-07 14:38:46.561872
5	25	borrow	1	2024-06-10 13:21:58.210096
4	25	borrow	1	2024-06-10 18:26:58.818171
\.


--
-- TOC entry 3400 (class 0 OID 0)
-- Dependencies: 220
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: library_pcou_user
--

SELECT pg_catalog.setval('public.books_id_seq', 25, true);


--
-- TOC entry 3401 (class 0 OID 0)
-- Dependencies: 216
-- Name: members_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: library_pcou_user
--

SELECT pg_catalog.setval('public.members_member_id_seq', 1, false);


--
-- TOC entry 3402 (class 0 OID 0)
-- Dependencies: 215
-- Name: staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: library_pcou_user
--

SELECT pg_catalog.setval('public.staff_id_seq', 9, true);


--
-- TOC entry 3403 (class 0 OID 0)
-- Dependencies: 218
-- Name: staff_staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: library_pcou_user
--

SELECT pg_catalog.setval('public.staff_staff_id_seq', 9, true);


--
-- TOC entry 3237 (class 2606 OID 16587)
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- TOC entry 3233 (class 2606 OID 16538)
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (member_id);


--
-- TOC entry 3235 (class 2606 OID 16560)
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (staff_id);


--
-- TOC entry 3238 (class 2606 OID 16614)
-- Name: transactions transactions_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id);


--
-- TOC entry 3239 (class 2606 OID 16594)
-- Name: transactions transactions_borrower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_borrower_id_fkey FOREIGN KEY (borrower_id) REFERENCES public.members(member_id);


--
-- TOC entry 3240 (class 2606 OID 16599)
-- Name: transactions transactions_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: library_pcou_user
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.staff(staff_id);


--
-- TOC entry 2054 (class 826 OID 16391)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO library_pcou_user;


--
-- TOC entry 2056 (class 826 OID 16393)
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO library_pcou_user;


--
-- TOC entry 2055 (class 826 OID 16392)
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO library_pcou_user;


--
-- TOC entry 2053 (class 826 OID 16390)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO library_pcou_user;


-- Completed on 2024-06-10 20:02:35

--
-- PostgreSQL database dump complete
--

