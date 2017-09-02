# -*- coding: utf-8 -*-
import os.path

import pygit2
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FileWritePipeline(object):
    def __init__(self, data_directory):
        self.data_directory = data_directory

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DATA_DIRECTORY'))

    def process_item(self, item, spider):
        data_directory = os.path.join(self.data_directory, spider.name)
        if not os.path.isdir(data_directory):
            os.makedirs(data_directory)
        with open(
            os.path.join(data_directory, '{}.txt'.format(item['title'])), 'w'
        ) as data_file:
            data_file.write('url: ')
            data_file.write(item['url'])
            data_file.write('\n------\n')
            data_file.write('\n')
            data_file.write(item['text'])

        return item


class GitCommitPipeline(object):
    def __init__(self, data_directory):
        self.repo = pygit2.Repository(os.path.abspath(data_directory))
        self.VALID_STATUSES = {
            pygit2.GIT_STATUS_WT_MODIFIED: 'Update',
            pygit2.GIT_STATUS_WT_NEW: 'Add',
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DATA_DIRECTORY'))

    def process_item(self, item, spider):
        for path, status in self.repo.status().items():
            if os.path.splitext(os.path.basename(path))[0] == item['title']\
                    and status in self.VALID_STATUSES.keys():
                action = self.VALID_STATUSES.get(status, 'Update')

                self.repo.index.add(path)
                self.repo.index.write()

                committer = pygit2.Signature(
                    spider.name, '{}@TosWatcher'.format(spider.name)
                )
                self.repo.create_commit(
                    self.repo.head.name,
                    committer,  # author
                    committer,
                    '{} {}'.format(action, path),
                    self.repo.index.write_tree(),
                    [self.repo.head.target]  # parents of the new commit
                )
                raise DropItem('Item processed')
