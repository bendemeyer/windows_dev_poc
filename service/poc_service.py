import time

from reporter import reporter
from service.base_service import SMWinservice


class POCService(SMWinservice):
    _svc_name_ = "WinDevPOC"
    _svc_display_name_ = "WinDevPOC Service"
    _svc_description_ = "Generate reports and such"

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def main(self):
        while self.is_running:
            reporter.run()
            time.sleep(60)


if __name__ == '__main__':
    POCService.parse_command_line()