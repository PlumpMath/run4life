#include "test.h"

using namespace std;

int main(int argc, char* argv[])
{
	cout << "Test Cerebrus" << endl;

	World* world=new World();
	Character* character=new Character();
	
	NavMesh* navmesh=world->get_nav_mesh();
	
	navmesh->load_file("navmesh.dat");
	for(int i=0;i<navmesh->get_num_nodes();++i){
		cout << navmesh->get_node(i)->to_string() << endl;
	}
	
	cout << "find closest node 1 (0,0,0) -> " << navmesh->find_closest_node(LPoint3f(0.0,0.0,0.0)) << endl;
	cout << "find closest node 2 (10,10,0) -> " << navmesh->find_closest_node(LPoint3f(10.0,10.0,0.0)) << endl;
	cout << "find path " << endl;
	navmesh->find_path_nodes(LPoint3f(0.0,0.0,0.0), LPoint3f(10.0,10.0,0.0));
	
	world->add_character(character);
	world->update();

	delete world;
}
