# crear un usuario mysql 
CREATE USER 'lobo_user'@'%' IDENTIFIED BY 'lobo_pass';

# otorgar privilegios sobre una BD , desde cualquier origen (IP) 
GRANT Create ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Alter ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Create view ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Delete ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Drop ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%' WITH GRANT OPTION;
GRANT Index ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Insert ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT References ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Select ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Show view ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Trigger ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Update ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Alter routine ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Create routine ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Create temporary tables ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Execute ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%';
GRANT Lock tables ON lobo_organizado_chkbkp.* TO 'lobo_user'@'%' WITH GRANT OPTION;