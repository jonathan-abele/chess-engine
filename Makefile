# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -shared -fPIC -std=c++11

# Output shared library
TARGET = engine.so

# Source files
SRCS = engine/engine.cpp engine/get_moves.cpp engine/engine_interface.cpp

# Default rule to build the shared library
all: $(TARGET)

# Build the shared library
$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRCS)

# Clean the output
clean:
	rm -f $(TARGET)
