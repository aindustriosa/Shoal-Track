--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Debian 10.4-2)
-- Dumped by pg_dump version 10.4 (Debian 10.4-2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: regatasolar3db; Type: DATABASE; Schema: -; Owner: regatasolar
--

CREATE DATABASE regatasolar3db WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'es_ES.UTF-8' LC_CTYPE = 'es_ES.UTF-8';


ALTER DATABASE regatasolar3db OWNER TO regatasolar;

\connect regatasolar3db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO regatasolar;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO regatasolar;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO regatasolar;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO regatasolar;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO regatasolar;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO regatasolar;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO regatasolar;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO regatasolar;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO regatasolar;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO regatasolar;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO regatasolar;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO regatasolar;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: chp_category; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_category (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    code character varying(10) NOT NULL,
    description character varying(255)
);


ALTER TABLE public.chp_category OWNER TO regatasolar;

--
-- Name: chp_category_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_category_id_seq OWNER TO regatasolar;

--
-- Name: chp_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_category_id_seq OWNED BY public.chp_category.id;


--
-- Name: chp_champion; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_champion (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    slug character varying(50) NOT NULL,
    edicion smallint NOT NULL,
    description character varying(255),
    timestamp_start timestamp with time zone NOT NULL,
    timestamp_finish timestamp with time zone,
    status smallint NOT NULL,
    image character varying(100),
    organization_id integer NOT NULL
);


ALTER TABLE public.chp_champion OWNER TO regatasolar;

--
-- Name: chp_champion_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_champion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_champion_id_seq OWNER TO regatasolar;

--
-- Name: chp_champion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_champion_id_seq OWNED BY public.chp_champion.id;


--
-- Name: chp_listrace; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_listrace (
    id integer NOT NULL,
    is_enable boolean NOT NULL,
    "order" smallint NOT NULL,
    champion_id integer NOT NULL,
    race_id integer NOT NULL
);


ALTER TABLE public.chp_listrace OWNER TO regatasolar;

--
-- Name: chp_listrace_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_listrace_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_listrace_id_seq OWNER TO regatasolar;

--
-- Name: chp_listrace_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_listrace_id_seq OWNED BY public.chp_listrace.id;


--
-- Name: chp_penalty; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_penalty (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(255),
    unit_type smallint NOT NULL
);


ALTER TABLE public.chp_penalty OWNER TO regatasolar;

--
-- Name: chp_penalty_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_penalty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_penalty_id_seq OWNER TO regatasolar;

--
-- Name: chp_penalty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_penalty_id_seq OWNED BY public.chp_penalty.id;


--
-- Name: chp_race; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_race (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    edicion smallint NOT NULL,
    slug character varying(50) NOT NULL,
    description character varying(255),
    timestamp_start timestamp with time zone NOT NULL,
    timestamp_finish timestamp with time zone,
    status smallint NOT NULL,
    limit_area public.geometry(Geometry,32629),
    image character varying(100),
    organization_id integer NOT NULL
);


ALTER TABLE public.chp_race OWNER TO regatasolar;

--
-- Name: chp_race_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_race_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_race_id_seq OWNER TO regatasolar;

--
-- Name: chp_race_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_race_id_seq OWNED BY public.chp_race.id;


--
-- Name: chp_racetrack; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_racetrack (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    color smallint NOT NULL,
    points double precision,
    timestamp_integrate timestamp with time zone NOT NULL,
    timestamp_exit timestamp with time zone,
    observations character varying(255),
    category_id integer,
    device_id integer NOT NULL,
    race_id integer NOT NULL
);


ALTER TABLE public.chp_racetrack OWNER TO regatasolar;

--
-- Name: chp_racetrack_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_racetrack_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_racetrack_id_seq OWNER TO regatasolar;

--
-- Name: chp_racetrack_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_racetrack_id_seq OWNED BY public.chp_racetrack.id;


--
-- Name: chp_trackgeom; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_trackgeom (
    id integer NOT NULL,
    timestamp_enable timestamp with time zone NOT NULL,
    track_pass smallint NOT NULL,
    timestamp_disable timestamp with time zone,
    "order" smallint NOT NULL,
    geom public.geometry(Geometry,32629),
    device_id integer NOT NULL,
    race_id integer NOT NULL
);


ALTER TABLE public.chp_trackgeom OWNER TO regatasolar;

--
-- Name: chp_trackgeom_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_trackgeom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_trackgeom_id_seq OWNER TO regatasolar;

--
-- Name: chp_trackgeom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_trackgeom_id_seq OWNED BY public.chp_trackgeom.id;


--
-- Name: chp_trackingnode; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_trackingnode (
    id integer NOT NULL,
    timestamp_pass timestamp with time zone NOT NULL,
    racetracking_id integer NOT NULL,
    trackgeom_id integer NOT NULL
);


ALTER TABLE public.chp_trackingnode OWNER TO regatasolar;

--
-- Name: chp_trackingnode_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_trackingnode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_trackingnode_id_seq OWNER TO regatasolar;

--
-- Name: chp_trackingnode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_trackingnode_id_seq OWNED BY public.chp_trackingnode.id;


--
-- Name: chp_trackingpenalty; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.chp_trackingpenalty (
    id integer NOT NULL,
    units smallint NOT NULL,
    timestamp_pass timestamp with time zone NOT NULL,
    description character varying(255),
    penalty_id integer NOT NULL,
    racetracking_id integer NOT NULL
);


ALTER TABLE public.chp_trackingpenalty OWNER TO regatasolar;

--
-- Name: chp_trackingpenalty_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.chp_trackingpenalty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chp_trackingpenalty_id_seq OWNER TO regatasolar;

--
-- Name: chp_trackingpenalty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.chp_trackingpenalty_id_seq OWNED BY public.chp_trackingpenalty.id;


--
-- Name: dev_node; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.dev_node (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    category smallint NOT NULL,
    acronym character varying(20) NOT NULL,
    description character varying(255),
    image character varying(100),
    weight double precision,
    length double precision,
    sleeve double precision,
    draft double precision,
    model3d character varying(100),
    timestamp_created timestamp with time zone NOT NULL,
    is_enable boolean NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE public.dev_node OWNER TO regatasolar;

--
-- Name: dev_node_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.dev_node_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dev_node_id_seq OWNER TO regatasolar;

--
-- Name: dev_node_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.dev_node_id_seq OWNED BY public.dev_node.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO regatasolar;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO regatasolar;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO regatasolar;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO regatasolar;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO regatasolar;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO regatasolar;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO regatasolar;

--
-- Name: msr_dataprocess; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.msr_dataprocess (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    type_equation smallint NOT NULL,
    type_param smallint NOT NULL,
    args character varying(200),
    device_id integer NOT NULL
);


ALTER TABLE public.msr_dataprocess OWNER TO regatasolar;

--
-- Name: msr_dataprocess_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.msr_dataprocess_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.msr_dataprocess_id_seq OWNER TO regatasolar;

--
-- Name: msr_dataprocess_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.msr_dataprocess_id_seq OWNED BY public.msr_dataprocess.id;


--
-- Name: msr_devdataraw; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.msr_devdataraw (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    timestamp_rcv timestamp with time zone NOT NULL,
    "nextHop" smallint NOT NULL,
    rssi smallint NOT NULL,
    geom public.geometry(Geometry,32629),
    gps_precision smallint NOT NULL,
    gps_itow bigint NOT NULL,
    gps_latitude double precision NOT NULL,
    gps_longitude double precision NOT NULL,
    gps_heading smallint NOT NULL,
    bearing_avg smallint NOT NULL,
    bearing_std smallint NOT NULL,
    voltage_batt_avg smallint NOT NULL,
    voltage_batt_std smallint NOT NULL,
    amp_batt_avg smallint NOT NULL,
    amp_batt_std smallint NOT NULL,
    pressure_avg smallint NOT NULL,
    pressure_std smallint NOT NULL,
    ligth_avg smallint NOT NULL,
    ligth_std smallint NOT NULL,
    "accX_avg" smallint NOT NULL,
    "accX_std" smallint NOT NULL,
    "accY_avg" smallint NOT NULL,
    "accY_std" smallint NOT NULL,
    "accZ_avg" smallint NOT NULL,
    "accZ_std" smallint NOT NULL,
    "gyrX_avg" smallint NOT NULL,
    "gyrX_std" smallint NOT NULL,
    "gyrY_avg" smallint NOT NULL,
    "gyrY_std" smallint NOT NULL,
    "gyrZ_avg" smallint NOT NULL,
    "gyrZ_std" smallint NOT NULL,
    ref_air_temp double precision,
    ref_pressure double precision,
    ref_humidity_relative double precision,
    ref_wind_module double precision,
    ref_wind_direction double precision,
    ranking smallint,
    velocity double precision,
    direction smallint,
    "accX_coef_id" integer,
    "accY_coef_id" integer,
    "accZ_coef_id" integer,
    amp_batt_coef_id integer,
    bearing_coef_id integer,
    device_id integer NOT NULL,
    "gyrX_coef_id" integer,
    "gyrY_coef_id" integer,
    "gyrZ_coef_id" integer,
    ligth_coef_id integer,
    pressure_coef_id integer,
    voltage_batt_coef_id integer
);


ALTER TABLE public.msr_devdataraw OWNER TO regatasolar;

--
-- Name: msr_devdataraw_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.msr_devdataraw_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.msr_devdataraw_id_seq OWNER TO regatasolar;

--
-- Name: msr_devdataraw_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.msr_devdataraw_id_seq OWNED BY public.msr_devdataraw.id;


--
-- Name: prf_contact; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.prf_contact (
    id integer NOT NULL,
    fisrt_name character varying(50) NOT NULL,
    last_name character varying(60) NOT NULL,
    acronym character varying(20) NOT NULL,
    email character varying(254),
    image character varying(100),
    user_id integer
);


ALTER TABLE public.prf_contact OWNER TO regatasolar;

--
-- Name: prf_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.prf_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prf_contact_id_seq OWNER TO regatasolar;

--
-- Name: prf_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.prf_contact_id_seq OWNED BY public.prf_contact.id;


--
-- Name: prf_monitor; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.prf_monitor (
    id integer NOT NULL,
    name character varying(60) NOT NULL,
    category smallint NOT NULL,
    image character varying(100),
    user_id integer
);


ALTER TABLE public.prf_monitor OWNER TO regatasolar;

--
-- Name: prf_monitor_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.prf_monitor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prf_monitor_id_seq OWNER TO regatasolar;

--
-- Name: prf_monitor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.prf_monitor_id_seq OWNED BY public.prf_monitor.id;


--
-- Name: prf_organization; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.prf_organization (
    id integer NOT NULL,
    name character varying(60) NOT NULL,
    acronym character varying(20) NOT NULL,
    country character varying(30),
    telephone character varying(30),
    email character varying(254),
    homepage character varying(200),
    image character varying(100)
);


ALTER TABLE public.prf_organization OWNER TO regatasolar;

--
-- Name: prf_organization_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.prf_organization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prf_organization_id_seq OWNER TO regatasolar;

--
-- Name: prf_organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.prf_organization_id_seq OWNED BY public.prf_organization.id;


--
-- Name: team_trace; Type: TABLE; Schema: public; Owner: regatasolar
--

CREATE TABLE public.team_trace (
    id integer NOT NULL,
    timestamp_enable timestamp with time zone NOT NULL,
    rol smallint NOT NULL,
    timestamp_disable timestamp with time zone,
    contact_id integer NOT NULL,
    device_id integer NOT NULL
);


ALTER TABLE public.team_trace OWNER TO regatasolar;

--
-- Name: team_trace_id_seq; Type: SEQUENCE; Schema: public; Owner: regatasolar
--

CREATE SEQUENCE public.team_trace_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.team_trace_id_seq OWNER TO regatasolar;

--
-- Name: team_trace_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: regatasolar
--

ALTER SEQUENCE public.team_trace_id_seq OWNED BY public.team_trace.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: chp_category id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_category ALTER COLUMN id SET DEFAULT nextval('public.chp_category_id_seq'::regclass);


--
-- Name: chp_champion id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_champion ALTER COLUMN id SET DEFAULT nextval('public.chp_champion_id_seq'::regclass);


--
-- Name: chp_listrace id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_listrace ALTER COLUMN id SET DEFAULT nextval('public.chp_listrace_id_seq'::regclass);


--
-- Name: chp_penalty id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_penalty ALTER COLUMN id SET DEFAULT nextval('public.chp_penalty_id_seq'::regclass);


--
-- Name: chp_race id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_race ALTER COLUMN id SET DEFAULT nextval('public.chp_race_id_seq'::regclass);


--
-- Name: chp_racetrack id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_racetrack ALTER COLUMN id SET DEFAULT nextval('public.chp_racetrack_id_seq'::regclass);


--
-- Name: chp_trackgeom id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackgeom ALTER COLUMN id SET DEFAULT nextval('public.chp_trackgeom_id_seq'::regclass);


--
-- Name: chp_trackingnode id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingnode ALTER COLUMN id SET DEFAULT nextval('public.chp_trackingnode_id_seq'::regclass);


--
-- Name: chp_trackingpenalty id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingpenalty ALTER COLUMN id SET DEFAULT nextval('public.chp_trackingpenalty_id_seq'::regclass);


--
-- Name: dev_node id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.dev_node ALTER COLUMN id SET DEFAULT nextval('public.dev_node_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: msr_dataprocess id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_dataprocess ALTER COLUMN id SET DEFAULT nextval('public.msr_dataprocess_id_seq'::regclass);


--
-- Name: msr_devdataraw id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw ALTER COLUMN id SET DEFAULT nextval('public.msr_devdataraw_id_seq'::regclass);


--
-- Name: prf_contact id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_contact ALTER COLUMN id SET DEFAULT nextval('public.prf_contact_id_seq'::regclass);


--
-- Name: prf_monitor id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_monitor ALTER COLUMN id SET DEFAULT nextval('public.prf_monitor_id_seq'::regclass);


--
-- Name: prf_organization id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_organization ALTER COLUMN id SET DEFAULT nextval('public.prf_organization_id_seq'::regclass);


--
-- Name: team_trace id; Type: DEFAULT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.team_trace ALTER COLUMN id SET DEFAULT nextval('public.team_trace_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add contacto	7	add_contact
20	Can change contacto	7	change_contact
21	Can delete contacto	7	delete_contact
22	Can add monitor	8	add_monitor
23	Can change monitor	8	change_monitor
24	Can delete monitor	8	delete_monitor
25	Can add organización	9	add_organization
26	Can change organización	9	change_organization
27	Can delete organización	9	delete_organization
28	Can add dispositivo	10	add_device
29	Can change dispositivo	10	change_device
30	Can delete dispositivo	10	delete_device
31	Can add trazabilidad del equipo	11	add_teamtrace
32	Can change trazabilidad del equipo	11	change_teamtrace
33	Can delete trazabilidad del equipo	11	delete_teamtrace
34	Can add campeonato	12	add_champion
35	Can change campeonato	12	change_champion
36	Can delete campeonato	12	delete_champion
37	Can add listado de carreras en campeonato	13	add_listtraceraces
38	Can change listado de carreras en campeonato	13	change_listtraceraces
39	Can delete listado de carreras en campeonato	13	delete_listtraceraces
40	Can add penalización	14	add_penalty
41	Can change penalización	14	change_penalty
42	Can delete penalización	14	delete_penalty
43	Can add monitorización de la penalización en la carrera	15	add_penaltytracking
44	Can change monitorización de la penalización en la carrera	15	change_penaltytracking
45	Can delete monitorización de la penalización en la carrera	15	delete_penaltytracking
46	Can add carrera	16	add_race
47	Can change carrera	16	change_race
48	Can delete carrera	16	delete_race
49	Can add categoría del participante	17	add_racecategory
50	Can change categoría del participante	17	change_racecategory
51	Can delete categoría del participante	17	delete_racecategory
52	Can add monitorización de la carrera	18	add_racetracking
53	Can change monitorización de la carrera	18	change_racetracking
54	Can delete monitorización de la carrera	18	delete_racetracking
55	Can add validacion de marcadores en la carrera	19	add_racetrackingnode
56	Can change validacion de marcadores en la carrera	19	change_racetrackingnode
57	Can delete validacion de marcadores en la carrera	19	delete_racetrackingnode
58	Can add marcador del trazado de la carrera	20	add_trackgeom
59	Can change marcador del trazado de la carrera	20	change_trackgeom
60	Can delete marcador del trazado de la carrera	20	delete_trackgeom
61	Can add coeficientes de proceso del dato	21	add_dataprocessing
62	Can change coeficientes de proceso del dato	21	change_dataprocessing
63	Can delete coeficientes de proceso del dato	21	delete_dataprocessing
64	Can add medida de dispositivo	22	add_devicedataraw
65	Can change medida de dispositivo	22	change_devicedataraw
66	Can delete medida de dispositivo	22	delete_devicedataraw
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$36000$Oho6qqW9qhim$qZy9U9uB/SNyPui9JoAgVl5Ic5laOn/aPhUYRo+vdrE=	2018-06-23 12:34:54.017349+02	t	rsolar			a@b.com	t	t	2018-06-23 12:33:46.627451+02
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: chp_category; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_category (id, name, code, description) FROM stdin;
1	Test	TST	Categoría No oficial para pruebas
2	Junior	JNR	Categoría de menores de 16 años
3	Senior	SNR	Categoría mayores de 16 años
4	Open	OPN	Categoría abierta a todo el mundo
\.


--
-- Data for Name: chp_champion; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_champion (id, name, slug, edicion, description, timestamp_start, timestamp_finish, status, image, organization_id) FROM stdin;
1	Regata Solar MarineInstruments	2-regata-solar-marineinstruments	2	Campeonato educacional de barcos propulsados por energia solar	2018-06-23 12:34:14.390299+02	\N	6	test_images/champion_logo.png	1
\.


--
-- Data for Name: chp_listrace; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_listrace (id, is_enable, "order", champion_id, race_id) FROM stdin;
1	t	1	1	1
2	t	2	1	2
3	t	3	1	3
4	t	4	1	4
\.


--
-- Data for Name: chp_penalty; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_penalty (id, name, description, unit_type) FROM stdin;
\.


--
-- Data for Name: chp_race; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_race (id, name, edicion, slug, description, timestamp_start, timestamp_finish, status, limit_area, image, organization_id) FROM stdin;
1	Test de Bouzas	1	1-test-de-bouzas	Test de pruebas integral	2018-06-23 12:34:14.406806+02	\N	3	0103000020757F000001000000050000007C8160365FC31F4154BA821963D55141E6E887B21AC41F41B698CCC367D55141BC4FFF0B9CC31F41E11C26B37BD55141746DDECB0CC31F415F1588D077D551417C8160365FC31F4154BA821963D55141	test_images/champion_1.jpg	1
4	Carrera de velocidad	1	1-carrera-de-velocidad	Una carrera de velocidad en linea recta	2018-06-23 12:34:14.435877+02	\N	3	0103000020757F0000010000000500000041EEBE0566481F41110D63D806CA5141B0881497D9461F41FA095AE0E7C951416C23DB5612481F413E6CA396D3C95141E43C4492334A1F41AE808E33F9C9514141EEBE0566481F41110D63D806CA5141	test_images/champion_2.jpg	1
2	Test de pruebas	1	1-test-de-pruebas	Test de pruebas para probar conceptos	2018-06-23 12:34:14+02	\N	10	0103000020757F0000010000000500000041EEBE0566481F41120D63D806CA5141B0881497D9461F41FA095AE0E7C951416C23DB5612481F413E6CA396D3C95141E43C4492334A1F41AF808E33F9C9514141EEBE0566481F41120D63D806CA5141	test_images/champion_1.jpg	1
3	Carrera de Resistencia	1	1-carrera-de-resistencia	Carrera con trayectorias de cruze	2018-06-23 12:34:14+02	\N	7	0103000020757F0000010000000500000041EEBE0566481F41120D63D806CA5141B0881497D9461F41FA095AE0E7C951416C23DB5612481F413E6CA396D3C95141E43C4492334A1F41AF808E33F9C9514141EEBE0566481F41120D63D806CA5141	test_images/champion_3.jpg	1
\.


--
-- Data for Name: chp_racetrack; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_racetrack (id, code, color, points, timestamp_integrate, timestamp_exit, observations, category_id, device_id, race_id) FROM stdin;
1	ASRS11	0	\N	2018-06-23 12:34:14.61999+02	\N	Un barquito	4	10	1
2	ASRS12	1	\N	2018-06-23 12:34:14.623596+02	\N	Un barquito	4	11	1
3	ASRS13	2	\N	2018-06-23 12:34:14.626458+02	\N	Un barquito	4	12	1
4	ASRS14	3	\N	2018-06-23 12:34:14.629363+02	\N	Un barquito	4	13	1
5	ASRS15	4	\N	2018-06-23 12:34:14.632359+02	\N	Un barquito	4	14	1
6	ASRS11	0	\N	2018-06-23 12:34:14.635399+02	\N	Un barquito	4	10	2
7	ASRS12	1	\N	2018-06-23 12:34:14.638377+02	\N	Un barquito	4	11	2
8	ASRS13	2	\N	2018-06-23 12:34:14.641214+02	\N	Un barquito	4	12	2
9	ASRS14	3	\N	2018-06-23 12:34:14.644213+02	\N	Un barquito	4	13	2
10	ASRS15	4	\N	2018-06-23 12:34:14.647225+02	\N	Un barquito	4	14	2
11	ASRS16	5	\N	2018-06-23 12:34:14.649966+02	\N	Un barquito	4	15	2
12	ASRS17	6	\N	2018-06-23 12:34:14.652793+02	\N	Un barquito	4	16	2
13	ASRS18	7	\N	2018-06-23 12:34:14.655748+02	\N	Un barquito	4	17	2
14	ASRS19	8	\N	2018-06-23 12:34:14.658645+02	\N	Un barquito	4	18	2
15	ASRS20	9	\N	2018-06-23 12:34:14.661535+02	\N	Un barquito	4	19	2
16	ASRS11	0	\N	2018-06-23 12:34:14.664374+02	\N	Un barquito	4	10	3
17	ASRS12	1	\N	2018-06-23 12:34:14.667163+02	\N	Un barquito	4	11	3
18	ASRS13	2	\N	2018-06-23 12:34:14.669971+02	\N	Un barquito	4	12	3
19	ASRS14	3	\N	2018-06-23 12:34:14.673545+02	\N	Un barquito	4	13	3
20	ASRS15	4	\N	2018-06-23 12:34:14.675956+02	\N	Un barquito	4	14	3
21	ASRS16	5	\N	2018-06-23 12:34:14.679119+02	\N	Un barquito	4	15	3
22	ASRS17	6	\N	2018-06-23 12:34:14.682316+02	\N	Un barquito	4	16	3
23	ASRS18	7	\N	2018-06-23 12:34:14.685555+02	\N	Un barquito	4	17	3
24	ASRS19	8	\N	2018-06-23 12:34:14.688222+02	\N	Un barquito	4	18	3
25	ASRS20	9	\N	2018-06-23 12:34:14.690688+02	\N	Un barquito	4	19	3
26	ASRS11	0	\N	2018-06-23 12:34:14.693096+02	\N	Un barquito	4	10	4
27	ASRS12	1	\N	2018-06-23 12:34:14.69556+02	\N	Un barquito	4	11	4
28	ASRS13	2	\N	2018-06-23 12:34:14.698181+02	\N	Un barquito	4	12	4
29	ASRS14	3	\N	2018-06-23 12:34:14.700728+02	\N	Un barquito	4	13	4
30	ASRS15	4	\N	2018-06-23 12:34:14.703147+02	\N	Un barquito	4	14	4
31	ASRS16	5	\N	2018-06-23 12:34:14.705579+02	\N	Un barquito	4	15	4
32	ASRS17	6	\N	2018-06-23 12:34:14.707968+02	\N	Un barquito	4	16	4
33	ASRS18	7	\N	2018-06-23 12:34:14.710479+02	\N	Un barquito	4	17	4
34	ASRS19	8	\N	2018-06-23 12:34:14.712976+02	\N	Un barquito	4	18	4
35	ASRS20	9	\N	2018-06-23 12:34:14.715373+02	\N	Un barquito	4	19	4
\.


--
-- Data for Name: chp_trackgeom; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_trackgeom (id, timestamp_enable, track_pass, timestamp_disable, "order", geom, device_id, race_id) FROM stdin;
1	2018-06-23 12:34:14.469178+02	0	\N	0	0101000020757F00008750260767C31F416551210966D55141	20	1
2	2018-06-23 12:34:14.474943+02	1	\N	0	0101000020757F00005CDD685DF6C31F4121BEB61668D55141	21	1
3	2018-06-23 12:34:14.482368+02	11	\N	1	0101000020757F00001008102B5FC31F41E601D1C476D55141	23	1
4	2018-06-23 12:34:14.48652+02	3	\N	2	0101000020757F00008750260767C31F416551210966D55141	20	1
5	2018-06-23 12:34:14.494557+02	2	\N	2	0101000020757F00005CDD685DF6C31F4121BEB61668D55141	21	1
6	2018-06-23 12:34:14.498701+02	200	\N	3	0101000020757F0000C0C1805183C41F414EDAE54977D55141	28	1
7	2018-06-23 12:34:14.50295+02	0	\N	0	0101000020757F00001CF262BE37471F4103BFBB05E9C95141	20	2
8	2018-06-23 12:34:14.506977+02	1	\N	0	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	2
9	2018-06-23 12:34:14.511119+02	17	\N	1	0101000020757F00008E96AC4785471F41AC6130DCEEC95141	22	2
10	2018-06-23 12:34:14.515076+02	11	\N	2	0101000020757F00006192D781D9471F41FB433CECF1C95141	23	2
11	2018-06-23 12:34:14.519178+02	13	\N	3	0101000020757F0000439DA306DD471F419B8DB56DEAC95141	24	2
12	2018-06-23 12:34:14.523164+02	3	\N	4	0101000020757F00001CF262BE37471F4103BFBB05E9C95141	20	2
13	2018-06-23 12:34:14.527115+02	2	\N	4	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	2
14	2018-06-23 12:34:14.531107+02	200	\N	5	0101000020757F00003F1B0E7D79461F414D651338F7C95141	28	2
15	2018-06-23 12:34:14.53486+02	0	\N	0	0101000020757F00001CF262BE37471F4103BFBB05E9C95141	20	3
16	2018-06-23 12:34:14.538632+02	1	\N	0	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	3
17	2018-06-23 12:34:14.542503+02	17	\N	1	0101000020757F00008E96AC4785471F41AC6130DCEEC95141	22	3
18	2018-06-23 12:34:14.546497+02	12	\N	2	0101000020757F00006192D781D9471F41FB433CECF1C95141	23	3
19	2018-06-23 12:34:14.550398+02	13	\N	3	0101000020757F0000439DA306DD471F419B8DB56DEAC95141	24	3
20	2018-06-23 12:34:14.554181+02	16	\N	4	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	3
21	2018-06-23 12:34:14.55789+02	17	\N	5	0101000020757F00008E96AC4785471F41AC6130DCEEC95141	22	3
22	2018-06-23 12:34:14.561727+02	12	\N	6	0101000020757F00006192D781D9471F41FB433CECF1C95141	23	3
23	2018-06-23 12:34:14.565565+02	13	\N	7	0101000020757F0000439DA306DD471F419B8DB56DEAC95141	24	3
24	2018-06-23 12:34:14.569287+02	16	\N	8	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	3
25	2018-06-23 12:34:14.574308+02	17	\N	9	0101000020757F00008E96AC4785471F41AC6130DCEEC95141	22	3
26	2018-06-23 12:34:14.578008+02	12	\N	10	0101000020757F00006192D781D9471F41FB433CECF1C95141	23	3
27	2018-06-23 12:34:14.581815+02	13	\N	11	0101000020757F0000439DA306DD471F419B8DB56DEAC95141	24	3
28	2018-06-23 12:34:14.585534+02	3	\N	12	0101000020757F00001CF262BE37471F4103BFBB05E9C95141	20	3
29	2018-06-23 12:34:14.589285+02	2	\N	13	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	3
30	2018-06-23 12:34:14.593185+02	200	\N	14	0101000020757F00003F1B0E7D79461F414D651338F7C95141	28	3
31	2018-06-23 12:34:14.597199+02	0	\N	0	0101000020757F00001CF262BE37471F4103BFBB05E9C95141	20	4
32	2018-06-23 12:34:14.601068+02	1	\N	0	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	4
33	2018-06-23 12:34:14.604826+02	11	\N	1	0101000020757F00006192D781D9471F41FB433CECF1C95141	23	4
34	2018-06-23 12:34:14.608826+02	3	\N	2	0101000020757F00001CF262BE37471F4103BFBB05E9C95141	20	4
35	2018-06-23 12:34:14.612748+02	2	\N	2	0101000020757F0000F76C6CF779471F415CC7E1B2E5C95141	21	4
36	2018-06-23 12:34:14.616604+02	200	\N	3	0101000020757F00003F1B0E7D79461F414D651338F7C95141	28	4
\.


--
-- Data for Name: chp_trackingnode; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_trackingnode (id, timestamp_pass, racetracking_id, trackgeom_id) FROM stdin;
\.


--
-- Data for Name: chp_trackingpenalty; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.chp_trackingpenalty (id, units, timestamp_pass, description, penalty_id, racetracking_id) FROM stdin;
\.


--
-- Data for Name: dev_node; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.dev_node (id, name, category, acronym, description, image, weight, length, sleeve, draft, model3d, timestamp_created, is_enable, owner_id) FROM stdin;
1	DC Team	6	ASRS03	Un bicasco con tradicional con motor encapsulado	test_images/boulder.png	600	4	3	3		2018-06-23 12:34:14.25256+02	t	2
2	Montecastelo Racing	0	ASRS05	Un vehiculo estilo planeador de fibra.	test_images/creepy.png	1400	5	4	6		2018-06-23 12:34:14.257319+02	t	3
3	Los apanados	1	ASRS04	Un catamaran normal 	test_images/convert.png	1200	6	4	8		2018-06-23 12:34:14.260917+02	t	2
4	Iluminados del Caribe	6	ASRS06	Es un trimaran pequeñito	test_images/rakuda.png	800	5	6	3		2018-06-23 12:34:14.264476+02	t	3
5	Hogar_1	6	ASRS07	Es un trimaran con forma de vaina pod de star wars	test_images/pussycat.png	500	3	3	2		2018-06-23 12:34:14.269597+02	t	4
6	Hogar_2	1	ASRS08	Un bicasco simple	test_images/army.png	2000	5	4	6		2018-06-23 12:34:14.274562+02	t	4
7	Os Secos	0	ASRS01	No se lo que es	test_images/bulletproof.png	1600	6	3	3		2018-06-23 12:34:14.281037+02	t	5
8	Naverga	0	ASRS02	Otro wue no he id a visitar	test_images/chuggabug.png	1100	4	3	3		2018-06-23 12:34:14.286184+02	t	5
9	MarineDor	1	ASRS09	Un bicaco con hidrofoil	test_images/turbo.png	450	6	2	1		2018-06-23 12:34:14.294802+02	t	6
10	OPRobots	0	ASRS11	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.298167+02	t	1
11	Taiyoken	0	ASRS12	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.302426+02	t	1
12	US613809	0	ASRS13	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.306733+02	t	1
13	Solarexpress	0	ASRS14	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.311538+02	t	1
14	Solar DS	0	ASRS15	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.316468+02	t	1
15	Vehiculo_Open_16	0	ASRS16	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.323315+02	t	1
16	BananaBoat	0	ASRS17	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.329174+02	t	1
17	Pirata	0	ASRS18	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.334559+02	t	1
18	Amigus Labs	0	ASRS19	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.348454+02	t	1
19	Vehiculo_Open_20	0	ASRS20	Una persona con un sensor en la cabeza	test_images/troncoswagen.png	690	3	3	3		2018-06-23 12:34:14.356126+02	t	1
20	VirtualMarkBuoy 01	100	VMRK01	Marca virtual de posicion para el inicio de la carrera	test_images/virtualbuoy.png	4	1	1	1		2018-06-23 12:34:14.36559+02	t	1
21	VirtualMarkBuoy 02	100	VMRK02	Marca virtual de posicion para el inicio de la carrera	test_images/virtualbuoy.png	4	1	1	1		2018-06-23 12:34:14.368639+02	t	1
22	VirtualMarkBuoy 03	100	VMRK03	Marca virtual de posicion para recorrido de la carrera	test_images/virtualbuoy.png	4	1	1	1		2018-06-23 12:34:14.371097+02	t	1
23	VirtualMarkBuoy 04	100	VMRK04	Marca virtual de posicion para recorrido de la carrera	test_images/virtualbuoy.png	4	1	1	1		2018-06-23 12:34:14.374303+02	t	1
24	VirtualMarkBuoy 05	100	VMRK05	Marca virtual de posicion para recorrido de la carrera	test_images/virtualbuoy.png	4	1	1	1		2018-06-23 12:34:14.376747+02	t	1
25	RaceMarkBuoy 01	101	RMRK01	Marca de posicion para la orientacion de la carrera	test_images/racebuoy.png	4	1	1	1		2018-06-23 12:34:14.379233+02	t	1
26	RaceMarkBuoy 02	101	RMRK02	Marca de posicion para la orientacion de la carrera	test_images/racebuoy.png	4	1	1	1		2018-06-23 12:34:14.381741+02	t	1
27	RaceMarkBuoy 03	101	RMRK03	Marca de posicion para la orientacion de la carrera	test_images/racebuoy.png	4	1	1	1		2018-06-23 12:34:14.384305+02	t	1
28	GatewayMark 01	102	GTWN01	Zona donde esta el concentrador principal	test_images/gate.png	4	1	1	1		2018-06-23 12:34:14.38688+02	t	1
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2018-06-23 12:35:06.759658+02	2	1ª Test de pruebas	2	[{"changed": {"fields": ["status"]}}]	16	1
2	2018-06-23 12:53:10.667464+02	2	1ª Test de pruebas	2	[{"changed": {"fields": ["status"]}}]	16	1
3	2018-06-23 12:56:08.071208+02	3	1ª Carrera de Resistencia	2	[{"changed": {"fields": ["status"]}}]	16	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	profiles	contact
8	profiles	monitor
9	profiles	organization
10	devices	device
11	devices	teamtrace
12	competition	champion
13	competition	listtraceraces
14	competition	penalty
15	competition	penaltytracking
16	competition	race
17	competition	racecategory
18	competition	racetracking
19	competition	racetrackingnode
20	competition	trackgeom
21	telemetrydata	dataprocessing
22	telemetrydata	devicedataraw
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2018-06-23 12:33:10.282142+02
2	auth	0001_initial	2018-06-23 12:33:10.360004+02
3	admin	0001_initial	2018-06-23 12:33:10.382966+02
4	admin	0002_logentry_remove_auto_add	2018-06-23 12:33:10.403492+02
5	contenttypes	0002_remove_content_type_name	2018-06-23 12:33:10.437728+02
6	auth	0002_alter_permission_name_max_length	2018-06-23 12:33:10.444904+02
7	auth	0003_alter_user_email_max_length	2018-06-23 12:33:10.458558+02
8	auth	0004_alter_user_username_opts	2018-06-23 12:33:10.470422+02
9	auth	0005_alter_user_last_login_null	2018-06-23 12:33:10.492886+02
10	auth	0006_require_contenttypes_0002	2018-06-23 12:33:10.496805+02
11	auth	0007_alter_validators_add_error_messages	2018-06-23 12:33:10.514056+02
12	auth	0008_alter_user_username_max_length	2018-06-23 12:33:10.537368+02
13	profiles	0001_initial	2018-06-23 12:33:10.590619+02
14	devices	0001_initial	2018-06-23 12:33:10.644088+02
15	competition	0001_initial	2018-06-23 12:33:11.005345+02
16	sessions	0001_initial	2018-06-23 12:33:11.014223+02
17	telemetrydata	0001_initial	2018-06-23 12:33:11.104979+02
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
4axmr7x9s64lpkmzih8hua736gqy3p6q	NzE0ZWZjNTJjMGEwZDEzMGVmYzQzOTAxZjliZGQ0NzM5ZmNjMjFlMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxNmY5NjkzZjBlODVmYTI3YjdiYmE5ZDM3ZTVlZWZjN2M5MTdmMGUyIn0=	2018-07-07 12:34:54.020093+02
\.


--
-- Data for Name: msr_dataprocess; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.msr_dataprocess (id, "timestamp", type_equation, type_param, args, device_id) FROM stdin;
1	2018-06-23 12:34:14.716572+02	0	0	[1, 0]	10
2	2018-06-23 12:34:14.71995+02	0	1	[1, 0]	10
3	2018-06-23 12:34:14.722515+02	1	2	[1, 0]	10
4	2018-06-23 12:34:14.724886+02	1	3	[1, 0]	10
5	2018-06-23 12:34:14.727238+02	1	4	[1, 0]	10
6	2018-06-23 12:34:14.729567+02	1	5	[1, 0]	10
7	2018-06-23 12:34:14.731815+02	1	6	[1, 0]	10
8	2018-06-23 12:34:14.734025+02	1	7	[1, 0]	10
9	2018-06-23 12:34:14.736194+02	1	8	[1, 0]	10
10	2018-06-23 12:34:14.738506+02	1	9	[1, 0]	10
11	2018-06-23 12:34:14.740719+02	1	10	[1, 0]	10
12	2018-06-23 12:34:14.742884+02	1	11	[1, 0]	10
13	2018-06-23 12:34:14.74531+02	1	12	[0.01, 0]	10
14	2018-06-23 12:34:14.747686+02	3	13	[1, 0]	10
15	2018-06-23 12:34:14.750057+02	1	14	[1, 0]	10
16	2018-06-23 12:34:14.752416+02	1	15	[0.023866, -1.18e-05]	10
17	2018-06-23 12:34:14.75476+02	1	16	[0.050934, -26.04537]	10
18	2018-06-23 12:34:14.7571+02	0	17	[1, 0]	10
19	2018-06-23 12:34:14.760408+02	0	18	[1, 0]	10
20	2018-06-23 12:34:14.762764+02	0	19	[1, 0]	10
21	2018-06-23 12:34:14.765116+02	0	0	[1, 0]	11
22	2018-06-23 12:34:14.767413+02	0	1	[1, 0]	11
23	2018-06-23 12:34:14.769682+02	1	2	[1, 0]	11
24	2018-06-23 12:34:14.773275+02	1	3	[1, 0]	11
25	2018-06-23 12:34:14.775566+02	1	4	[1, 0]	11
26	2018-06-23 12:34:14.77797+02	1	5	[1, 0]	11
27	2018-06-23 12:34:14.780431+02	1	6	[1, 0]	11
28	2018-06-23 12:34:14.782891+02	1	7	[1, 0]	11
29	2018-06-23 12:34:14.785463+02	1	8	[1, 0]	11
30	2018-06-23 12:34:14.788092+02	1	9	[1, 0]	11
31	2018-06-23 12:34:14.790644+02	1	10	[1, 0]	11
32	2018-06-23 12:34:14.792992+02	1	11	[1, 0]	11
33	2018-06-23 12:34:14.795445+02	1	12	[0.01, 0]	11
34	2018-06-23 12:34:14.797821+02	3	13	[1, 0]	11
35	2018-06-23 12:34:14.800139+02	1	14	[1, 0]	11
36	2018-06-23 12:34:14.802537+02	1	15	[0.023866, -1.18e-05]	11
37	2018-06-23 12:34:14.804957+02	1	16	[0.050934, -26.04537]	11
38	2018-06-23 12:34:14.807237+02	0	17	[1, 0]	11
39	2018-06-23 12:34:14.809502+02	0	18	[1, 0]	11
40	2018-06-23 12:34:14.811889+02	0	19	[1, 0]	11
41	2018-06-23 12:34:14.81419+02	0	0	[1, 0]	12
42	2018-06-23 12:34:14.816456+02	0	1	[1, 0]	12
43	2018-06-23 12:34:14.818694+02	1	2	[1, 0]	12
44	2018-06-23 12:34:14.820948+02	1	3	[1, 0]	12
45	2018-06-23 12:34:14.823197+02	1	4	[1, 0]	12
46	2018-06-23 12:34:14.825454+02	1	5	[1, 0]	12
47	2018-06-23 12:34:14.827631+02	1	6	[1, 0]	12
48	2018-06-23 12:34:14.829746+02	1	7	[1, 0]	12
49	2018-06-23 12:34:14.831882+02	1	8	[1, 0]	12
50	2018-06-23 12:34:14.834238+02	1	9	[1, 0]	12
51	2018-06-23 12:34:14.836486+02	1	10	[1, 0]	12
52	2018-06-23 12:34:14.83854+02	1	11	[1, 0]	12
53	2018-06-23 12:34:14.840593+02	1	12	[0.01, 0]	12
54	2018-06-23 12:34:14.842995+02	3	13	[1, 0]	12
55	2018-06-23 12:34:14.845442+02	1	14	[1, 0]	12
56	2018-06-23 12:34:14.84781+02	1	15	[0.023866, -1.18e-05]	12
57	2018-06-23 12:34:14.850169+02	1	16	[0.050934, -26.04537]	12
58	2018-06-23 12:34:14.852457+02	0	17	[1, 0]	12
59	2018-06-23 12:34:14.854805+02	0	18	[1, 0]	12
60	2018-06-23 12:34:14.857153+02	0	19	[1, 0]	12
61	2018-06-23 12:34:14.859391+02	0	0	[1, 0]	13
62	2018-06-23 12:34:14.861657+02	0	1	[1, 0]	13
63	2018-06-23 12:34:14.863913+02	1	2	[1, 0]	13
64	2018-06-23 12:34:14.866155+02	1	3	[1, 0]	13
65	2018-06-23 12:34:14.868457+02	1	4	[1, 0]	13
66	2018-06-23 12:34:14.872002+02	1	5	[1, 0]	13
67	2018-06-23 12:34:14.874425+02	1	6	[1, 0]	13
68	2018-06-23 12:34:14.876774+02	1	7	[1, 0]	13
69	2018-06-23 12:34:14.879103+02	1	8	[1, 0]	13
70	2018-06-23 12:34:14.881599+02	1	9	[1, 0]	13
71	2018-06-23 12:34:14.88407+02	1	10	[1, 0]	13
72	2018-06-23 12:34:14.886633+02	1	11	[1, 0]	13
73	2018-06-23 12:34:14.889137+02	1	12	[0.01, 0]	13
74	2018-06-23 12:34:14.891615+02	3	13	[1, 0]	13
75	2018-06-23 12:34:14.894066+02	1	14	[1, 0]	13
76	2018-06-23 12:34:14.896286+02	1	15	[0.023866, -1.18e-05]	13
77	2018-06-23 12:34:14.898559+02	1	16	[0.050934, -26.04537]	13
78	2018-06-23 12:34:14.900786+02	0	17	[1, 0]	13
79	2018-06-23 12:34:14.903047+02	0	18	[1, 0]	13
80	2018-06-23 12:34:14.905354+02	0	19	[1, 0]	13
81	2018-06-23 12:34:14.90766+02	0	0	[1, 0]	14
82	2018-06-23 12:34:14.909993+02	0	1	[1, 0]	14
83	2018-06-23 12:34:14.91232+02	1	2	[1, 0]	14
84	2018-06-23 12:34:14.914666+02	1	3	[1, 0]	14
85	2018-06-23 12:34:14.916991+02	1	4	[1, 0]	14
86	2018-06-23 12:34:14.919291+02	1	5	[1, 0]	14
87	2018-06-23 12:34:14.921614+02	1	6	[1, 0]	14
88	2018-06-23 12:34:14.923921+02	1	7	[1, 0]	14
89	2018-06-23 12:34:14.926232+02	1	8	[1, 0]	14
90	2018-06-23 12:34:14.928446+02	1	9	[1, 0]	14
91	2018-06-23 12:34:14.930696+02	1	10	[1, 0]	14
92	2018-06-23 12:34:14.932951+02	1	11	[1, 0]	14
93	2018-06-23 12:34:14.935209+02	1	12	[0.01, 0]	14
94	2018-06-23 12:34:14.937461+02	3	13	[1, 0]	14
95	2018-06-23 12:34:14.939756+02	1	14	[1, 0]	14
96	2018-06-23 12:34:14.942072+02	1	15	[0.023866, -1.18e-05]	14
97	2018-06-23 12:34:14.944509+02	1	16	[0.050934, -26.04537]	14
98	2018-06-23 12:34:14.946912+02	0	17	[1, 0]	14
99	2018-06-23 12:34:14.949227+02	0	18	[1, 0]	14
100	2018-06-23 12:34:14.951542+02	0	19	[1, 0]	14
101	2018-06-23 12:34:14.953848+02	0	0	[1, 0]	15
102	2018-06-23 12:34:14.956168+02	0	1	[1, 0]	15
103	2018-06-23 12:34:14.958441+02	1	2	[1, 0]	15
104	2018-06-23 12:34:14.960778+02	1	3	[1, 0]	15
105	2018-06-23 12:34:14.963085+02	1	4	[1, 0]	15
106	2018-06-23 12:34:14.965406+02	1	5	[1, 0]	15
107	2018-06-23 12:34:14.967728+02	1	6	[1, 0]	15
108	2018-06-23 12:34:14.9701+02	1	7	[1, 0]	15
109	2018-06-23 12:34:14.973294+02	1	8	[1, 0]	15
110	2018-06-23 12:34:14.975643+02	1	9	[1, 0]	15
111	2018-06-23 12:34:14.978052+02	1	10	[1, 0]	15
112	2018-06-23 12:34:14.980456+02	1	11	[1, 0]	15
113	2018-06-23 12:34:14.982874+02	1	12	[0.01, 0]	15
114	2018-06-23 12:34:14.985327+02	3	13	[1, 0]	15
115	2018-06-23 12:34:14.987677+02	1	14	[1, 0]	15
116	2018-06-23 12:34:14.990045+02	1	15	[0.023866, -1.18e-05]	15
117	2018-06-23 12:34:14.992288+02	1	16	[0.050934, -26.04537]	15
118	2018-06-23 12:34:14.994604+02	0	17	[1, 0]	15
119	2018-06-23 12:34:14.9969+02	0	18	[1, 0]	15
120	2018-06-23 12:34:14.999097+02	0	19	[1, 0]	15
121	2018-06-23 12:34:15.001256+02	0	0	[1, 0]	16
122	2018-06-23 12:34:15.003304+02	0	1	[1, 0]	16
123	2018-06-23 12:34:15.005373+02	1	2	[1, 0]	16
124	2018-06-23 12:34:15.007531+02	1	3	[1, 0]	16
125	2018-06-23 12:34:15.010121+02	1	4	[1, 0]	16
126	2018-06-23 12:34:15.012447+02	1	5	[1, 0]	16
127	2018-06-23 12:34:15.014546+02	1	6	[1, 0]	16
128	2018-06-23 12:34:15.016779+02	1	7	[1, 0]	16
129	2018-06-23 12:34:15.019392+02	1	8	[1, 0]	16
130	2018-06-23 12:34:15.021809+02	1	9	[1, 0]	16
131	2018-06-23 12:34:15.024185+02	1	10	[1, 0]	16
132	2018-06-23 12:34:15.026699+02	1	11	[1, 0]	16
133	2018-06-23 12:34:15.029122+02	1	12	[0.01, 0]	16
134	2018-06-23 12:34:15.031592+02	3	13	[1, 0]	16
135	2018-06-23 12:34:15.034018+02	1	14	[1, 0]	16
136	2018-06-23 12:34:15.036359+02	1	15	[0.023866, -1.18e-05]	16
137	2018-06-23 12:34:15.038718+02	1	16	[0.050934, -26.04537]	16
138	2018-06-23 12:34:15.041034+02	0	17	[1, 0]	16
139	2018-06-23 12:34:15.043371+02	0	18	[1, 0]	16
140	2018-06-23 12:34:15.045875+02	0	19	[1, 0]	16
141	2018-06-23 12:34:15.048207+02	0	0	[1, 0]	17
142	2018-06-23 12:34:15.050517+02	0	1	[1, 0]	17
143	2018-06-23 12:34:15.05286+02	1	2	[1, 0]	17
144	2018-06-23 12:34:15.055234+02	1	3	[1, 0]	17
145	2018-06-23 12:34:15.057557+02	1	4	[1, 0]	17
146	2018-06-23 12:34:15.059897+02	1	5	[1, 0]	17
147	2018-06-23 12:34:15.062241+02	1	6	[1, 0]	17
148	2018-06-23 12:34:15.064628+02	1	7	[1, 0]	17
149	2018-06-23 12:34:15.066964+02	1	8	[1, 0]	17
150	2018-06-23 12:34:15.069266+02	1	9	[1, 0]	17
151	2018-06-23 12:34:15.073282+02	1	10	[1, 0]	17
152	2018-06-23 12:34:15.075836+02	1	11	[1, 0]	17
153	2018-06-23 12:34:15.078348+02	1	12	[0.01, 0]	17
154	2018-06-23 12:34:15.080933+02	3	13	[1, 0]	17
155	2018-06-23 12:34:15.083422+02	1	14	[1, 0]	17
156	2018-06-23 12:34:15.085883+02	1	15	[0.023866, -1.18e-05]	17
157	2018-06-23 12:34:15.08815+02	1	16	[0.050934, -26.04537]	17
158	2018-06-23 12:34:15.090328+02	0	17	[1, 0]	17
159	2018-06-23 12:34:15.0928+02	0	18	[1, 0]	17
160	2018-06-23 12:34:15.095135+02	0	19	[1, 0]	17
161	2018-06-23 12:34:15.097484+02	0	0	[1, 0]	18
162	2018-06-23 12:34:15.09981+02	0	1	[1, 0]	18
163	2018-06-23 12:34:15.102105+02	1	2	[1, 0]	18
164	2018-06-23 12:34:15.104481+02	1	3	[1, 0]	18
165	2018-06-23 12:34:15.106848+02	1	4	[1, 0]	18
166	2018-06-23 12:34:15.109158+02	1	5	[1, 0]	18
167	2018-06-23 12:34:15.111494+02	1	6	[1, 0]	18
168	2018-06-23 12:34:15.113812+02	1	7	[1, 0]	18
169	2018-06-23 12:34:15.116129+02	1	8	[1, 0]	18
170	2018-06-23 12:34:15.118472+02	1	9	[1, 0]	18
171	2018-06-23 12:34:15.120783+02	1	10	[1, 0]	18
172	2018-06-23 12:34:15.123121+02	1	11	[1, 0]	18
173	2018-06-23 12:34:15.125442+02	1	12	[0.01, 0]	18
174	2018-06-23 12:34:15.127732+02	3	13	[1, 0]	18
175	2018-06-23 12:34:15.129996+02	1	14	[1, 0]	18
176	2018-06-23 12:34:15.132259+02	1	15	[0.023866, -1.18e-05]	18
177	2018-06-23 12:34:15.134542+02	1	16	[0.050934, -26.04537]	18
178	2018-06-23 12:34:15.136768+02	0	17	[1, 0]	18
179	2018-06-23 12:34:15.13908+02	0	18	[1, 0]	18
180	2018-06-23 12:34:15.141389+02	0	19	[1, 0]	18
181	2018-06-23 12:34:15.143697+02	0	0	[1, 0]	19
182	2018-06-23 12:34:15.146146+02	0	1	[1, 0]	19
183	2018-06-23 12:34:15.14849+02	1	2	[1, 0]	19
184	2018-06-23 12:34:15.150766+02	1	3	[1, 0]	19
185	2018-06-23 12:34:15.153011+02	1	4	[1, 0]	19
186	2018-06-23 12:34:15.155251+02	1	5	[1, 0]	19
187	2018-06-23 12:34:15.15751+02	1	6	[1, 0]	19
188	2018-06-23 12:34:15.159732+02	1	7	[1, 0]	19
189	2018-06-23 12:34:15.162099+02	1	8	[1, 0]	19
190	2018-06-23 12:34:15.164403+02	1	9	[1, 0]	19
191	2018-06-23 12:34:15.166688+02	1	10	[1, 0]	19
192	2018-06-23 12:34:15.16897+02	1	11	[1, 0]	19
193	2018-06-23 12:34:15.172063+02	1	12	[0.01, 0]	19
194	2018-06-23 12:34:15.174498+02	3	13	[1, 0]	19
195	2018-06-23 12:34:15.176935+02	1	14	[1, 0]	19
196	2018-06-23 12:34:15.179315+02	1	15	[0.023866, -1.18e-05]	19
197	2018-06-23 12:34:15.182044+02	1	16	[0.050934, -26.04537]	19
198	2018-06-23 12:34:15.184431+02	0	17	[1, 0]	19
199	2018-06-23 12:34:15.18677+02	0	18	[1, 0]	19
200	2018-06-23 12:34:15.189136+02	0	19	[1, 0]	19
\.


--
-- Data for Name: msr_devdataraw; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.msr_devdataraw (id, "timestamp", timestamp_rcv, "nextHop", rssi, geom, gps_precision, gps_itow, gps_latitude, gps_longitude, gps_heading, bearing_avg, bearing_std, voltage_batt_avg, voltage_batt_std, amp_batt_avg, amp_batt_std, pressure_avg, pressure_std, ligth_avg, ligth_std, "accX_avg", "accX_std", "accY_avg", "accY_std", "accZ_avg", "accZ_std", "gyrX_avg", "gyrX_std", "gyrY_avg", "gyrY_std", "gyrZ_avg", "gyrZ_std", ref_air_temp, ref_pressure, ref_humidity_relative, ref_wind_module, ref_wind_direction, ranking, velocity, direction, "accX_coef_id", "accY_coef_id", "accZ_coef_id", amp_batt_coef_id, bearing_coef_id, device_id, "gyrX_coef_id", "gyrY_coef_id", "gyrZ_coef_id", ligth_coef_id, pressure_coef_id, voltage_batt_coef_id) FROM stdin;
1	2018-06-23 12:35:07.30642+02	2018-06-23 12:35:07.306438+02	-1	0	0101000020757F000000D8FFFFFF3F7FC0FEFFFFFFFF3F7FC0	-1	-1	-500	-500	-1	-1	-1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N	\N	\N	\N	\N	28	\N	\N	\N	\N	\N	\N
2	2018-06-23 12:56:08.790077+02	2018-06-23 12:56:08.790098+02	-1	0	0101000020757F000000D8FFFFFF3F7FC0FEFFFFFFFF3F7FC0	-1	-1	-500	-500	-1	-1	-1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N	\N	\N	\N	\N	28	\N	\N	\N	\N	\N	\N
3	2018-06-23 13:01:06+02	2018-06-23 13:01:09.01631+02	0	0	0101000020757F000033EEEC35BC461F418305C486EBC95141	7	558078500	4663214.10571420565	512431.052661630267	0	-1	-1	856	0	10	0	167	0	118	0	61	32	-161	32	525	48	12	16	-2	0	0	16	0	0	0	0	0	0	0.0262415968271133074	173	63	64	65	77	\N	13	66	67	68	74	72	76
\.


--
-- Data for Name: prf_contact; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.prf_contact (id, fisrt_name, last_name, acronym, email, image, user_id) FROM stdin;
1	Piedro	Macana	macana	pmacana@mac.com	test_images/piedro_macana.png	\N
2	Roco	Macana	macanito	rmacana@mac.com	test_images/roco_macana.png	\N
3	Humanoide	Corpulento	giganton	hcorpul@mac.com	test_images/human.png	\N
4	Vampiro	Púrpura	vampi	vampi@mac.com	test_images/vamp.png	\N
5	Pat	Locovitch	profesor	plocovitch@mac.com	test_images/locovitch.png	\N
6	Hans	Fritz	red max	redmax@mac.com	test_images/hans.png	\N
7	Penélope	Glamour	pitstop	pglamour@mac.com	test_images/penelope.png	\N
8	Sargento	Blast	sargento	sblea@stmac.com	test_images/blast.png	\N
9	Soldado	Meekly	soldadito	meekly@mac.com	test_images/meekly.png	\N
10	Mafio	Hormin	mafio	mhormin@mac.com	test_images/mafio.png	\N
11	Luiggi	Hormin	cosquillas	lhormin@mac.com	test_images/mafio_1.png	\N
12	Petrus	Hormin	acero	phormin@mac.com	test_images/mafio_2.png	\N
13	Julius	Hormin	pequeñin	jhormin@mac.com	test_images/mafio_3.png	\N
14	Riggo	Hormin	escape	rhormin@mac.com	test_images/mafio_4.png	\N
15	Antonio	Hormin	gatillo	ahormin@mac.com	test_images/mafio_5.png	\N
16	Éolo	Hormin	risitas	ehormin@mac.com	test_images/mafio_6.png	\N
17	Luke	Granjer	granjero	lgranj@mac.com	test_images/luke.png	\N
18	Blubber	Bear	miedoso	bbear@mac.com	test_images/bear.png	\N
19	Pedro	Bello	pedrito	pbello@mac.com	test_images/bello.png	\N
20	Rufus	Ruffcut	Brutus	rruff@mac.com	test_images/brutus.png	\N
21	Castor	Sawtooth	Listus	csawtoo@mac.com	test_images/listus.png	\N
22	Dick	Dastardly	Nodoyuna	dnodoyuna@mac.com	test_images/pierre.png	\N
23	Perro	Muttley	Patán	ppatan@mac.com	test_images/patan.png	\N
\.


--
-- Data for Name: prf_monitor; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.prf_monitor (id, name, category, image, user_id) FROM stdin;
\.


--
-- Data for Name: prf_organization; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.prf_organization (id, name, acronym, country, telephone, email, homepage, image) FROM stdin;
1	Organizacion	ORGNZT	Galicia	543678905	equipo@utmar.org	www.mi.com	test_images/organization.png
2	Colegio Daniel Castelao	CDCEPS	Galicia	543678905	ijia@iji.com	www.ht.com	test_images/mafia.png
3	Colegio Montecastelo	CMTCEP	Galicia	23491913	ijia@avff.com	www.hsfv.org	test_images/tenebroso.png
4	Colegio Hogar	CHRCEPS	Galicia	9484838	ijia@adadca.es	www.adadca.es	test_images/maker.png
5	Escuelas Proval	EPVCEP	Galicia	543678905	ijia@iji.com	www.ht.com	test_images/es111.png
6	MarineInstruments	MARINST	Galicia	543678905	ijia@iji.com	www.ht.com	test_images/es111.png
7	AIndustriosa	AINDUST	Galicia	543678905	ijia@iji.com	www.ht.com	test_images/es111.png
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: team_trace; Type: TABLE DATA; Schema: public; Owner: regatasolar
--

COPY public.team_trace (id, timestamp_enable, rol, timestamp_disable, contact_id, device_id) FROM stdin;
1	2018-06-23 12:34:14.254478+02	8	\N	1	1
2	2018-06-23 12:34:14.258685+02	8	\N	3	2
3	2018-06-23 12:34:14.262251+02	8	\N	5	3
4	2018-06-23 12:34:14.265801+02	8	\N	6	4
5	2018-06-23 12:34:14.272019+02	8	\N	7	5
6	2018-06-23 12:34:14.275926+02	8	\N	8	6
7	2018-06-23 12:34:14.277163+02	8	\N	9	6
8	2018-06-23 12:34:14.282747+02	8	\N	10	7
9	2018-06-23 12:34:14.284006+02	8	\N	11	7
10	2018-06-23 12:34:14.28781+02	8	\N	17	8
11	2018-06-23 12:34:14.292597+02	8	\N	18	8
12	2018-06-23 12:34:14.296046+02	8	\N	19	9
13	2018-06-23 12:34:14.299418+02	8	\N	20	10
14	2018-06-23 12:34:14.300412+02	8	\N	21	10
15	2018-06-23 12:34:14.303651+02	8	\N	20	11
16	2018-06-23 12:34:14.304722+02	8	\N	21	11
17	2018-06-23 12:34:14.308154+02	8	\N	20	12
18	2018-06-23 12:34:14.309313+02	8	\N	21	12
19	2018-06-23 12:34:14.313034+02	8	\N	20	13
20	2018-06-23 12:34:14.314261+02	8	\N	21	13
21	2018-06-23 12:34:14.317936+02	8	\N	20	14
22	2018-06-23 12:34:14.3194+02	8	\N	21	14
23	2018-06-23 12:34:14.324902+02	8	\N	20	15
24	2018-06-23 12:34:14.326092+02	8	\N	21	15
25	2018-06-23 12:34:14.331199+02	8	\N	20	16
26	2018-06-23 12:34:14.332277+02	8	\N	21	16
27	2018-06-23 12:34:14.336607+02	8	\N	20	17
28	2018-06-23 12:34:14.342342+02	8	\N	21	17
29	2018-06-23 12:34:14.350195+02	8	\N	20	18
30	2018-06-23 12:34:14.353265+02	8	\N	21	18
31	2018-06-23 12:34:14.357743+02	8	\N	20	19
32	2018-06-23 12:34:14.359075+02	8	\N	21	19
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 66, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: chp_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_category_id_seq', 4, true);


--
-- Name: chp_champion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_champion_id_seq', 1, true);


--
-- Name: chp_listrace_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_listrace_id_seq', 4, true);


--
-- Name: chp_penalty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_penalty_id_seq', 1, false);


--
-- Name: chp_race_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_race_id_seq', 4, true);


--
-- Name: chp_racetrack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_racetrack_id_seq', 35, true);


--
-- Name: chp_trackgeom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_trackgeom_id_seq', 36, true);


--
-- Name: chp_trackingnode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_trackingnode_id_seq', 1, false);


--
-- Name: chp_trackingpenalty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.chp_trackingpenalty_id_seq', 1, false);


--
-- Name: dev_node_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.dev_node_id_seq', 28, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 3, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 22, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 17, true);


--
-- Name: msr_dataprocess_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.msr_dataprocess_id_seq', 200, true);


--
-- Name: msr_devdataraw_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.msr_devdataraw_id_seq', 3, true);


--
-- Name: prf_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.prf_contact_id_seq', 23, true);


--
-- Name: prf_monitor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.prf_monitor_id_seq', 1, false);


--
-- Name: prf_organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.prf_organization_id_seq', 7, true);


--
-- Name: team_trace_id_seq; Type: SEQUENCE SET; Schema: public; Owner: regatasolar
--

SELECT pg_catalog.setval('public.team_trace_id_seq', 32, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: chp_category chp_category_code_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_category
    ADD CONSTRAINT chp_category_code_key UNIQUE (code);


--
-- Name: chp_category chp_category_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_category
    ADD CONSTRAINT chp_category_pkey PRIMARY KEY (id);


--
-- Name: chp_champion chp_champion_name_edicion_d3dd4e01_uniq; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_champion
    ADD CONSTRAINT chp_champion_name_edicion_d3dd4e01_uniq UNIQUE (name, edicion);


--
-- Name: chp_champion chp_champion_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_champion
    ADD CONSTRAINT chp_champion_pkey PRIMARY KEY (id);


--
-- Name: chp_champion chp_champion_slug_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_champion
    ADD CONSTRAINT chp_champion_slug_key UNIQUE (slug);


--
-- Name: chp_listrace chp_listrace_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_listrace
    ADD CONSTRAINT chp_listrace_pkey PRIMARY KEY (id);


--
-- Name: chp_penalty chp_penalty_name_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_penalty
    ADD CONSTRAINT chp_penalty_name_key UNIQUE (name);


--
-- Name: chp_penalty chp_penalty_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_penalty
    ADD CONSTRAINT chp_penalty_pkey PRIMARY KEY (id);


--
-- Name: chp_race chp_race_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_race
    ADD CONSTRAINT chp_race_pkey PRIMARY KEY (id);


--
-- Name: chp_race chp_race_slug_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_race
    ADD CONSTRAINT chp_race_slug_key UNIQUE (slug);


--
-- Name: chp_racetrack chp_racetrack_device_id_race_id_code_5a232031_uniq; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_racetrack
    ADD CONSTRAINT chp_racetrack_device_id_race_id_code_5a232031_uniq UNIQUE (device_id, race_id, code);


--
-- Name: chp_racetrack chp_racetrack_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_racetrack
    ADD CONSTRAINT chp_racetrack_pkey PRIMARY KEY (id);


--
-- Name: chp_trackgeom chp_trackgeom_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackgeom
    ADD CONSTRAINT chp_trackgeom_pkey PRIMARY KEY (id);


--
-- Name: chp_trackingnode chp_trackingnode_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingnode
    ADD CONSTRAINT chp_trackingnode_pkey PRIMARY KEY (id);


--
-- Name: chp_trackingpenalty chp_trackingpenalty_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingpenalty
    ADD CONSTRAINT chp_trackingpenalty_pkey PRIMARY KEY (id);


--
-- Name: dev_node dev_node_acronym_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.dev_node
    ADD CONSTRAINT dev_node_acronym_key UNIQUE (acronym);


--
-- Name: dev_node dev_node_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.dev_node
    ADD CONSTRAINT dev_node_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: msr_dataprocess msr_dataprocess_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_dataprocess
    ADD CONSTRAINT msr_dataprocess_pkey PRIMARY KEY (id);


--
-- Name: msr_devdataraw msr_devdataraw_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT msr_devdataraw_pkey PRIMARY KEY (id);


--
-- Name: prf_contact prf_contact_acronym_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_contact
    ADD CONSTRAINT prf_contact_acronym_key UNIQUE (acronym);


--
-- Name: prf_contact prf_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_contact
    ADD CONSTRAINT prf_contact_pkey PRIMARY KEY (id);


--
-- Name: prf_monitor prf_monitor_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_monitor
    ADD CONSTRAINT prf_monitor_pkey PRIMARY KEY (id);


--
-- Name: prf_organization prf_organization_acronym_key; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_organization
    ADD CONSTRAINT prf_organization_acronym_key UNIQUE (acronym);


--
-- Name: prf_organization prf_organization_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_organization
    ADD CONSTRAINT prf_organization_pkey PRIMARY KEY (id);


--
-- Name: team_trace team_trace_pkey; Type: CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.team_trace
    ADD CONSTRAINT team_trace_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: chp_category_code_0455aa14_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_category_code_0455aa14_like ON public.chp_category USING btree (code varchar_pattern_ops);


--
-- Name: chp_champion_organization_id_589a3d07; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_champion_organization_id_589a3d07 ON public.chp_champion USING btree (organization_id);


--
-- Name: chp_champion_slug_23756c69_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_champion_slug_23756c69_like ON public.chp_champion USING btree (slug varchar_pattern_ops);


--
-- Name: chp_listrace_champion_id_e5dd15da; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_listrace_champion_id_e5dd15da ON public.chp_listrace USING btree (champion_id);


--
-- Name: chp_listrace_race_id_0454c8ee; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_listrace_race_id_0454c8ee ON public.chp_listrace USING btree (race_id);


--
-- Name: chp_penalty_name_2eba5854_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_penalty_name_2eba5854_like ON public.chp_penalty USING btree (name varchar_pattern_ops);


--
-- Name: chp_race_limit_area_id; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_race_limit_area_id ON public.chp_race USING gist (limit_area);


--
-- Name: chp_race_organization_id_037247e3; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_race_organization_id_037247e3 ON public.chp_race USING btree (organization_id);


--
-- Name: chp_race_slug_9d1e3236_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_race_slug_9d1e3236_like ON public.chp_race USING btree (slug varchar_pattern_ops);


--
-- Name: chp_racetrack_category_id_95ed1307; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_racetrack_category_id_95ed1307 ON public.chp_racetrack USING btree (category_id);


--
-- Name: chp_racetrack_device_id_c713cdb9; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_racetrack_device_id_c713cdb9 ON public.chp_racetrack USING btree (device_id);


--
-- Name: chp_racetrack_race_id_6e143ff3; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_racetrack_race_id_6e143ff3 ON public.chp_racetrack USING btree (race_id);


--
-- Name: chp_trackgeom_device_id_57d11a71; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_trackgeom_device_id_57d11a71 ON public.chp_trackgeom USING btree (device_id);


--
-- Name: chp_trackgeom_geom_id; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_trackgeom_geom_id ON public.chp_trackgeom USING gist (geom);


--
-- Name: chp_trackgeom_race_id_8cc51822; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_trackgeom_race_id_8cc51822 ON public.chp_trackgeom USING btree (race_id);


--
-- Name: chp_trackingnode_racetracking_id_7dd623df; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_trackingnode_racetracking_id_7dd623df ON public.chp_trackingnode USING btree (racetracking_id);


--
-- Name: chp_trackingnode_trackgeom_id_93c8bd11; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_trackingnode_trackgeom_id_93c8bd11 ON public.chp_trackingnode USING btree (trackgeom_id);


--
-- Name: chp_trackingpenalty_penalty_id_97240047; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_trackingpenalty_penalty_id_97240047 ON public.chp_trackingpenalty USING btree (penalty_id);


--
-- Name: chp_trackingpenalty_racetracking_id_f234f653; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX chp_trackingpenalty_racetracking_id_f234f653 ON public.chp_trackingpenalty USING btree (racetracking_id);


--
-- Name: dev_node_acronym_db5b8920_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX dev_node_acronym_db5b8920_like ON public.dev_node USING btree (acronym varchar_pattern_ops);


--
-- Name: dev_node_owner_id_9158af61; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX dev_node_owner_id_9158af61 ON public.dev_node USING btree (owner_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: msr_dataprocess_device_id_ff40b298; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_dataprocess_device_id_ff40b298 ON public.msr_dataprocess USING btree (device_id);


--
-- Name: msr_devdataraw_accX_coef_id_781f86c0; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX "msr_devdataraw_accX_coef_id_781f86c0" ON public.msr_devdataraw USING btree ("accX_coef_id");


--
-- Name: msr_devdataraw_accY_coef_id_7837cb94; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX "msr_devdataraw_accY_coef_id_7837cb94" ON public.msr_devdataraw USING btree ("accY_coef_id");


--
-- Name: msr_devdataraw_accZ_coef_id_da9a3bd8; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX "msr_devdataraw_accZ_coef_id_da9a3bd8" ON public.msr_devdataraw USING btree ("accZ_coef_id");


--
-- Name: msr_devdataraw_amp_batt_coef_id_85f8ad78; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_devdataraw_amp_batt_coef_id_85f8ad78 ON public.msr_devdataraw USING btree (amp_batt_coef_id);


--
-- Name: msr_devdataraw_bearing_coef_id_5ba4274e; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_devdataraw_bearing_coef_id_5ba4274e ON public.msr_devdataraw USING btree (bearing_coef_id);


--
-- Name: msr_devdataraw_device_id_4bbad2d1; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_devdataraw_device_id_4bbad2d1 ON public.msr_devdataraw USING btree (device_id);


--
-- Name: msr_devdataraw_geom_id; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_devdataraw_geom_id ON public.msr_devdataraw USING gist (geom);


--
-- Name: msr_devdataraw_gyrX_coef_id_539b1a73; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX "msr_devdataraw_gyrX_coef_id_539b1a73" ON public.msr_devdataraw USING btree ("gyrX_coef_id");


--
-- Name: msr_devdataraw_gyrY_coef_id_3d3f1483; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX "msr_devdataraw_gyrY_coef_id_3d3f1483" ON public.msr_devdataraw USING btree ("gyrY_coef_id");


--
-- Name: msr_devdataraw_gyrZ_coef_id_45263cb5; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX "msr_devdataraw_gyrZ_coef_id_45263cb5" ON public.msr_devdataraw USING btree ("gyrZ_coef_id");


--
-- Name: msr_devdataraw_ligth_coef_id_5c34ac50; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_devdataraw_ligth_coef_id_5c34ac50 ON public.msr_devdataraw USING btree (ligth_coef_id);


--
-- Name: msr_devdataraw_pressure_coef_id_5738d8f3; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_devdataraw_pressure_coef_id_5738d8f3 ON public.msr_devdataraw USING btree (pressure_coef_id);


--
-- Name: msr_devdataraw_voltage_batt_coef_id_9a70f7f1; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX msr_devdataraw_voltage_batt_coef_id_9a70f7f1 ON public.msr_devdataraw USING btree (voltage_batt_coef_id);


--
-- Name: prf_contact_acronym_89ac6076_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX prf_contact_acronym_89ac6076_like ON public.prf_contact USING btree (acronym varchar_pattern_ops);


--
-- Name: prf_contact_user_id_fcc3c0da; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX prf_contact_user_id_fcc3c0da ON public.prf_contact USING btree (user_id);


--
-- Name: prf_monitor_user_id_c6c4304c; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX prf_monitor_user_id_c6c4304c ON public.prf_monitor USING btree (user_id);


--
-- Name: prf_organization_acronym_edf54c22_like; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX prf_organization_acronym_edf54c22_like ON public.prf_organization USING btree (acronym varchar_pattern_ops);


--
-- Name: team_trace_contact_id_2aabbd77; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX team_trace_contact_id_2aabbd77 ON public.team_trace USING btree (contact_id);


--
-- Name: team_trace_device_id_5485e77a; Type: INDEX; Schema: public; Owner: regatasolar
--

CREATE INDEX team_trace_device_id_5485e77a ON public.team_trace USING btree (device_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_champion chp_champion_organization_id_589a3d07_fk_prf_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_champion
    ADD CONSTRAINT chp_champion_organization_id_589a3d07_fk_prf_organization_id FOREIGN KEY (organization_id) REFERENCES public.prf_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_listrace chp_listrace_champion_id_e5dd15da_fk_chp_champion_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_listrace
    ADD CONSTRAINT chp_listrace_champion_id_e5dd15da_fk_chp_champion_id FOREIGN KEY (champion_id) REFERENCES public.chp_champion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_listrace chp_listrace_race_id_0454c8ee_fk_chp_race_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_listrace
    ADD CONSTRAINT chp_listrace_race_id_0454c8ee_fk_chp_race_id FOREIGN KEY (race_id) REFERENCES public.chp_race(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_race chp_race_organization_id_037247e3_fk_prf_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_race
    ADD CONSTRAINT chp_race_organization_id_037247e3_fk_prf_organization_id FOREIGN KEY (organization_id) REFERENCES public.prf_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_racetrack chp_racetrack_category_id_95ed1307_fk_chp_category_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_racetrack
    ADD CONSTRAINT chp_racetrack_category_id_95ed1307_fk_chp_category_id FOREIGN KEY (category_id) REFERENCES public.chp_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_racetrack chp_racetrack_device_id_c713cdb9_fk_dev_node_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_racetrack
    ADD CONSTRAINT chp_racetrack_device_id_c713cdb9_fk_dev_node_id FOREIGN KEY (device_id) REFERENCES public.dev_node(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_racetrack chp_racetrack_race_id_6e143ff3_fk_chp_race_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_racetrack
    ADD CONSTRAINT chp_racetrack_race_id_6e143ff3_fk_chp_race_id FOREIGN KEY (race_id) REFERENCES public.chp_race(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_trackgeom chp_trackgeom_device_id_57d11a71_fk_dev_node_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackgeom
    ADD CONSTRAINT chp_trackgeom_device_id_57d11a71_fk_dev_node_id FOREIGN KEY (device_id) REFERENCES public.dev_node(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_trackgeom chp_trackgeom_race_id_8cc51822_fk_chp_race_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackgeom
    ADD CONSTRAINT chp_trackgeom_race_id_8cc51822_fk_chp_race_id FOREIGN KEY (race_id) REFERENCES public.chp_race(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_trackingnode chp_trackingnode_racetracking_id_7dd623df_fk_chp_racetrack_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingnode
    ADD CONSTRAINT chp_trackingnode_racetracking_id_7dd623df_fk_chp_racetrack_id FOREIGN KEY (racetracking_id) REFERENCES public.chp_racetrack(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_trackingnode chp_trackingnode_trackgeom_id_93c8bd11_fk_chp_trackgeom_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingnode
    ADD CONSTRAINT chp_trackingnode_trackgeom_id_93c8bd11_fk_chp_trackgeom_id FOREIGN KEY (trackgeom_id) REFERENCES public.chp_trackgeom(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_trackingpenalty chp_trackingpenalty_penalty_id_97240047_fk_chp_penalty_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingpenalty
    ADD CONSTRAINT chp_trackingpenalty_penalty_id_97240047_fk_chp_penalty_id FOREIGN KEY (penalty_id) REFERENCES public.chp_penalty(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chp_trackingpenalty chp_trackingpenalty_racetracking_id_f234f653_fk_chp_racet; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.chp_trackingpenalty
    ADD CONSTRAINT chp_trackingpenalty_racetracking_id_f234f653_fk_chp_racet FOREIGN KEY (racetracking_id) REFERENCES public.chp_racetrack(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dev_node dev_node_owner_id_9158af61_fk_prf_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.dev_node
    ADD CONSTRAINT dev_node_owner_id_9158af61_fk_prf_organization_id FOREIGN KEY (owner_id) REFERENCES public.prf_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_dataprocess msr_dataprocess_device_id_ff40b298_fk_dev_node_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_dataprocess
    ADD CONSTRAINT msr_dataprocess_device_id_ff40b298_fk_dev_node_id FOREIGN KEY (device_id) REFERENCES public.dev_node(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_accX_coef_id_781f86c0_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT "msr_devdataraw_accX_coef_id_781f86c0_fk_msr_dataprocess_id" FOREIGN KEY ("accX_coef_id") REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_accY_coef_id_7837cb94_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT "msr_devdataraw_accY_coef_id_7837cb94_fk_msr_dataprocess_id" FOREIGN KEY ("accY_coef_id") REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_accZ_coef_id_da9a3bd8_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT "msr_devdataraw_accZ_coef_id_da9a3bd8_fk_msr_dataprocess_id" FOREIGN KEY ("accZ_coef_id") REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_amp_batt_coef_id_85f8ad78_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT msr_devdataraw_amp_batt_coef_id_85f8ad78_fk_msr_dataprocess_id FOREIGN KEY (amp_batt_coef_id) REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_bearing_coef_id_5ba4274e_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT msr_devdataraw_bearing_coef_id_5ba4274e_fk_msr_dataprocess_id FOREIGN KEY (bearing_coef_id) REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_device_id_4bbad2d1_fk_dev_node_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT msr_devdataraw_device_id_4bbad2d1_fk_dev_node_id FOREIGN KEY (device_id) REFERENCES public.dev_node(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_gyrX_coef_id_539b1a73_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT "msr_devdataraw_gyrX_coef_id_539b1a73_fk_msr_dataprocess_id" FOREIGN KEY ("gyrX_coef_id") REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_gyrY_coef_id_3d3f1483_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT "msr_devdataraw_gyrY_coef_id_3d3f1483_fk_msr_dataprocess_id" FOREIGN KEY ("gyrY_coef_id") REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_gyrZ_coef_id_45263cb5_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT "msr_devdataraw_gyrZ_coef_id_45263cb5_fk_msr_dataprocess_id" FOREIGN KEY ("gyrZ_coef_id") REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_ligth_coef_id_5c34ac50_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT msr_devdataraw_ligth_coef_id_5c34ac50_fk_msr_dataprocess_id FOREIGN KEY (ligth_coef_id) REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_pressure_coef_id_5738d8f3_fk_msr_dataprocess_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT msr_devdataraw_pressure_coef_id_5738d8f3_fk_msr_dataprocess_id FOREIGN KEY (pressure_coef_id) REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: msr_devdataraw msr_devdataraw_voltage_batt_coef_id_9a70f7f1_fk_msr_datap; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.msr_devdataraw
    ADD CONSTRAINT msr_devdataraw_voltage_batt_coef_id_9a70f7f1_fk_msr_datap FOREIGN KEY (voltage_batt_coef_id) REFERENCES public.msr_dataprocess(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: prf_contact prf_contact_user_id_fcc3c0da_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_contact
    ADD CONSTRAINT prf_contact_user_id_fcc3c0da_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: prf_monitor prf_monitor_user_id_c6c4304c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.prf_monitor
    ADD CONSTRAINT prf_monitor_user_id_c6c4304c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: team_trace team_trace_contact_id_2aabbd77_fk_prf_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.team_trace
    ADD CONSTRAINT team_trace_contact_id_2aabbd77_fk_prf_contact_id FOREIGN KEY (contact_id) REFERENCES public.prf_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: team_trace team_trace_device_id_5485e77a_fk_dev_node_id; Type: FK CONSTRAINT; Schema: public; Owner: regatasolar
--

ALTER TABLE ONLY public.team_trace
    ADD CONSTRAINT team_trace_device_id_5485e77a_fk_dev_node_id FOREIGN KEY (device_id) REFERENCES public.dev_node(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

