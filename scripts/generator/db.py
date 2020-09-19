import time
import datetime
from typing import Any, Dict, List, Optional, Tuple

from geopy import distance as geopy_distance  # type: ignore
from geopy.geocoders import Nominatim
import polyline  # type: ignore
from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    PickleType,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from stravalib.model import Activity as StravaActivity  # type: ignore

from .valuerange import ValueRange


Base = declarative_base()


# reverse the location (lan, lon) -> location detail
g = Nominatim(user_agent="yihong0618")


ACTIVITY_KEYS = [
    "run_id",
    "name",
    "distance",
    "moving_time",
    "type",
    "start_date",
    "start_date_local",
    "location_country",
    "summary_polyline",
    "average_heartrate",
    "average_speed",
]


class Activity(Base):
    __tablename__ = "activities"

    run_id = Column(Integer, primary_key=True)
    name = Column(String)
    distance = Column(Float)
    moving_time = Column(Interval)
    elapsed_time = Column(Interval)
    type = Column(String)
    start_date = Column(String)
    start_date_local = Column(String)
    location_country = Column(String)
    summary_polyline = Column(String)
    average_heartrate =  Column(Float)
    average_speed =  Column(Float)
    streak = None

    def to_dict(self) -> Dict:
        out: Dict[str, Any] = {}
        for key in ACTIVITY_KEYS:
            attr = getattr(self, key)
            if isinstance(attr, (datetime.timedelta, datetime.datetime)):
                out[key] = str(attr)
            else:
                out[key] = attr

        if self.streak:
            out["streak"] = self.streak

        return out


def update_or_create_activity(session, run_activity):
    created = False
    activity = session.query(Activity).filter_by(run_id=int(run_activity.id)).first()
    if not activity:
        start_point = run_activity.start_latlng
        location_country = ""
        if start_point:
            try:
                location_country = str(g.reverse(f"{start_point.lat}, {start_point.lon}"))
            # limit (only for the first time)
            except:
                print("+++++++limit+++++++")
                time.sleep(60)
                location_country = str(g.reverse(f"{start_point.lat}, {start_point.lon}"))
                
            
        activity = Activity(
            run_id=run_activity.id,
            name=run_activity.name,
            distance=run_activity.distance,
            moving_time=run_activity.moving_time,
            elapsed_time=run_activity.elapsed_time,
            type=run_activity.type,
            start_date=run_activity.start_date,
            start_date_local=run_activity.start_date_local,
            location_country=location_country,
            average_heartrate=run_activity.average_heartrate,
            average_speed=float(run_activity.average_speed),
        )
        session.add(activity)
        created = True
    else:
        activity.name = run_activity.name
        activity.distance = float(run_activity.distance)
        activity.moving_time = run_activity.moving_time
        activity.elapsed_time = run_activity.elapsed_time
        activity.type = run_activity.type
        activity.average_heartrate=run_activity.average_heartrate
        activity.average_speed=float(run_activity.average_speed)
    try:
        activity.summary_polyline = run_activity.map.summary_polyline
    # just for gpx use 
    except:
        activity.summary_polyline = run_activity.polyline_str

    return created


def init_db(db_path: str) -> Session:
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()