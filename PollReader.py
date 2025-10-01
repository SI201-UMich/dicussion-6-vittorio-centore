import os
import unittest


class PollReader():
    """
    a class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        """
        the constructor. opens up the specified file, reads in the data,
        closes the file handler, and sets up the data dictionary that will be
        populated with build_data_dict().
        """

        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.full_path = os.path.join(self.base_path, filename)

        self.file_obj = open(self.full_path, 'r')
        self.raw_data = self.file_obj.readlines()
        self.file_obj.close()

        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
        """
        reads the csv data and builds a dictionary of columns
        """

        # skip the header row
        for i, line in enumerate(self.raw_data):
            if i == 0:
                continue

            # split by comma, not space
            separated = line.strip().split(',')

            self.data_dict['month'].append(separated[0])
            self.data_dict['date'].append(int(separated[1]))
            self.data_dict['sample'].append(int(separated[2]))
            self.data_dict['sample type'].append(separated[3])
            self.data_dict['Harris result'].append(float(separated[4]))
            self.data_dict['Trump result'].append(float(separated[5]))

    def highest_polling_candidate(self):
        """
        find candidate with highest single polling percentage
        """

        max_harris = max(self.data_dict['Harris result'])
        max_trump = max(self.data_dict['Trump result'])

        if max_harris > max_trump:
            return f"Harris {max_harris*100:.1f}%"
        elif max_trump > max_harris:
            return f"Trump {max_trump*100:.1f}%"
        else:
            return f"EVEN {max_harris*100:.1f}%"

    def likely_voter_polling_average(self):
        """
        average results for harris and trump among likely voters (lv)
        """

        harris_lv = []
        trump_lv = []

        for i, sample_type in enumerate(self.data_dict['sample type']):
            if sample_type == 'LV':
                harris_lv.append(self.data_dict['Harris result'][i])
                trump_lv.append(self.data_dict['Trump result'][i])

        harris_avg = sum(harris_lv) / len(harris_lv)
        trump_avg = sum(trump_lv) / len(trump_lv)

        return harris_avg, trump_avg

    def polling_history_change(self):
        """
        change in averages between earliest 30 and latest 30 polls
        """

        harris_early = self.data_dict['Harris result'][:30]
        trump_early = self.data_dict['Trump result'][:30]
        harris_late = self.data_dict['Harris result'][-30:]
        trump_late = self.data_dict['Trump result'][-30:]

        harris_early_avg = sum(harris_early) / len(harris_early)
        trump_early_avg = sum(trump_early) / len(trump_early)
        harris_late_avg = sum(harris_late) / len(harris_late)
        trump_late_avg = sum(trump_late) / len(trump_late)

        harris_change = harris_late_avg - harris_early_avg
        trump_change = trump_late_avg - trump_early_avg

        return harris_change, trump_change


class TestPollReader(unittest.TestCase):
    """
    test cases for pollreader
    """
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result or "Trump" in result or "EVEN" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))


def main():
    poll_reader = PollReader('polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")

    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")

    # comment

    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")


if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
