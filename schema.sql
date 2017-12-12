drop table if exists images;
create table images (
  id integer primary key autoincrement,
  title text not null,
  pic_date text not null,
  centroid_lat double not null,
  centroid_lon double not null,
  url text not null
);