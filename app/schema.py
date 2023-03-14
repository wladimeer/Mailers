instructions = [
    'drop table if exists email;'
    '''
        create table email(
            id int not null auto_increment,
            address text not null,
            subject text not null,
            content text not null,
            primary key(id)
        );
    '''
]