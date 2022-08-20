from http import HTTPStatus

from django.test import TestCase

from .models import Group, Lecturer, Room


class TestGroupViewSet(TestCase):
    name = "Name"
    subgroups = 1

    def setUp(self):
        g = Group()
        g.name = self.name
        g.subgroups = self.subgroups
        g.save()

    def test_group_get_list(self):
        res = self.client.get('/api/groups/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, [{
            'id': 1,
            'name': self.name,
            'subgroups': self.subgroups,
        }])

    def test_group_get_existing(self):
        res = self.client.get('/api/groups/1/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, {
            'id': 1,
            'name': self.name,
            'subgroups': self.subgroups,
        })

    def test_group_get_absent(self):
        res = self.client.get('/api/groups/2/')
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)


class TestRoomViewSet(TestCase):
    num = "1"

    def setUp(self):
        r = Room()
        r.num = self.num
        r.save()

    def test_room_get_list(self):
        res = self.client.get('/api/rooms/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, [{
            'id': 1,
            'num': self.num,
        }])

    def test_room_get_existing(self):
        res = self.client.get('/api/rooms/1/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, {
            'id': 1,
            'num': self.num,
        })

    def test_room_get_absent(self):
        res = self.client.get('/api/rooms/2/')
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)


class TestLecturerViewSet(TestCase):
    name = "Name"

    def setUp(self):
        lecturer = Lecturer()
        lecturer.name = self.name
        lecturer.save()

    def test_lecturer_get_list(self):
        res = self.client.get('/api/lecturers/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, [{
            'id': 1,
            'name': self.name,
        }])

    def test_lecturer_get_existing(self):
        res = self.client.get('/api/lecturers/1/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, {
            'id': 1,
            'name': self.name,
        })

    def test_lecturer_get_absent(self):
        res = self.client.get('/api/lecturers/2/')
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
