.PHONY: init all clean

init: 
	@echo "Init the Project..."
	@echo "Python venv start up..."
	@python3 -m venv ./venv
	@echo "The venv is init done..."
	@source ./venv/bin/activate
	@echo "stage 1 done..."

run: init


all:
	@echo "Building all needed items..."
	@make init
	@make run

clean:
	@echo "Cleaning up..."
	rm -rf ./venv