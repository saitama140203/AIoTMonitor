"""Re-Initial models

Revision ID: d16e554a7662
Revises: ccb6cbe7ed9e
Create Date: 2025-04-16 11:58:57.007346

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd16e554a7662'
down_revision: Union[str, None] = 'ccb6cbe7ed9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    # Tạo bảng groups
    op.create_table('groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_actived', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Tạo bảng profiles với khóa ngoại group_id
    op.create_table('profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table('commands',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('commands_text', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('username', sa.String(length=50), nullable=True, unique=True),
        sa.Column('ip', sa.String(length=50), nullable=True),
        sa.Column('port', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('platform', sa.String(length=100), nullable=True),
        sa.Column('lastseen', sa.DateTime(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('profile_user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=True),
        sa.Column('operator_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['operator_id'], ['users.id']),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('user_role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('activity_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(), nullable=True),
        sa.Column('details', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('command_profile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=True),
        sa.Column('command_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['command_id'], ['commands.id']),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Seed dữ liệu
    roles_table = sa.table('roles',
        sa.column('name', sa.String),
        sa.column('description', sa.String)
    )
    op.bulk_insert(roles_table, [
        {'name': 'admin', 'description': 'Quản trị hệ thống'},
        {'name': 'operator', 'description': 'Người vận hành'},
        {'name': 'supervisor', 'description': 'Giám sát viên'},
        {'name': 'team_lead', 'description': 'Trưởng nhóm'}
    ])

    users_table = sa.table('users',
        sa.column('username', sa.String),
        sa.column('email', sa.String),
        sa.column('full_name', sa.String),
        sa.column('hashed_password', sa.String),
        sa.column('is_active', sa.Boolean)
    )
    op.bulk_insert(users_table, [
        {
            'username': 'admin',
            'email': 'admin@aiotmonitor.com',
            'full_name': 'Administrator',
            'hashed_password': '$2b$12$/olbAOLO/ECDHvoP3ETrd.vPTUI2lJF6Dw9.lMzndIDgorHPIouCa',
            'is_active': True
        }
    ])

    commands_table = sa.table('commands',
        sa.column('commands_text', sa.String),
        sa.column('description', sa.String),
    )
    op.bulk_insert(commands_table, [
        {"commands_text": "ls", "description": "List files"},
        {"commands_text": "pwd", "description": "Print working directory"},
        {"commands_text": "whoami", "description": "Show current user"},
        {"commands_text": "df -h", "description": "Show disk space"},
        {"commands_text": "top", "description": "Show running processes"},
        {"commands_text": "ps aux", "description": "Show process list"},
        {"commands_text": "uptime", "description": "System uptime"},
        {"commands_text": "free -m", "description": "Show memory usage"},
        {"commands_text": "ifconfig", "description": "Network interfaces"},
        {"commands_text": "netstat -tuln", "description": "Listening ports"},
        {"commands_text": "reboot", "description": "Reboot the system"},
        {"commands_text": "shutdown now", "description": "Shutdown system"},
        {"commands_text": "mkdir test", "description": "Create directory"},
        {"commands_text": "rm -rf test", "description": "Remove directory"},
        {"commands_text": "touch file.txt", "description": "Create file"},
        {"commands_text": "cat file.txt", "description": "View file"},
        {"commands_text": "tail -f log.txt", "description": "Follow logs"},
        {"commands_text": "chmod +x script.sh", "description": "Make script executable"},
        {"commands_text": "ping 8.8.8.8", "description": "Ping Google DNS"}
    ])

    # Gán role admin
    connection = op.get_bind()
    admin_role = connection.execute(sa.text("SELECT id FROM roles WHERE name = 'admin'")).fetchone()
    admin_user = connection.execute(sa.text("SELECT id FROM users WHERE username = 'admin'")).fetchone()

    if admin_role and admin_user:
        user_role_table = sa.table('user_role',
            sa.column('user_id', sa.Integer),
            sa.column('role_id', sa.Integer)
        )
        op.bulk_insert(user_role_table, [{'user_id': admin_user[0], 'role_id': admin_role[0]}])


def downgrade() -> None:
    op.drop_table('command_profile')
    op.drop_table('activity_logs')
    op.drop_table('user_role')
    op.drop_table('profile_user')
    op.drop_table('devices')
    op.drop_table('commands')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('profiles')
    op.drop_table('groups')
