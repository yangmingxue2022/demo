from flask import Blueprint, request, jsonify, abort
from db import db
from models import Story, Bug, Iteration, Release

api_bp = Blueprint('api', __name__)

def obj_to_dict(obj, include_relations=False):
    if obj is None:
        return None
    data = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        data[col.name] = val.isoformat() if hasattr(val, 'isoformat') else val
    if include_relations:
        if isinstance(obj, Story):
            data['bugs'] = [obj_to_dict(b) for b in obj.bugs]
    return data

@api_bp.route('/stories', methods=['GET'])
def list_stories():
    stories = Story.query.all()
    return jsonify([obj_to_dict(s, include_relations=True) for s in stories])

@api_bp.route('/stories/<int:story_id>', methods=['GET'])
def get_story(story_id):
    s = Story.query.get_or_404(story_id)
    return jsonify(obj_to_dict(s, include_relations=True))

@api_bp.route('/stories', methods=['POST'])
def create_story():
    data = request.get_json() or {}
    if 'title' not in data:
        abort(400, 'title required')
    s = Story(title=data['title'], description=data.get('description'), status=data.get('status','open'), points=data.get('points',0))
    db.session.add(s)
    db.session.commit()
    return jsonify(obj_to_dict(s)), 201

@api_bp.route('/stories/<int:story_id>', methods=['PUT'])
def update_story(story_id):
    s = Story.query.get_or_404(story_id)
    data = request.get_json() or {}
    for k in ('title','description','status','points','iteration_id','release_id'):
        if k in data:
            setattr(s, k, data[k])
    db.session.commit()
    return jsonify(obj_to_dict(s))

@api_bp.route('/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    s = Story.query.get_or_404(story_id)
    db.session.delete(s)
    db.session.commit()
    return '', 204

# Bugs
@api_bp.route('/bugs', methods=['GET'])
def list_bugs():
    bugs = Bug.query.all()
    return jsonify([obj_to_dict(b) for b in bugs])

@api_bp.route('/bugs', methods=['POST'])
def create_bug():
    data = request.get_json() or {}
    if 'title' not in data:
        abort(400, 'title required')
    b = Bug(title=data['title'], description=data.get('description'), status=data.get('status','open'), severity=data.get('severity','medium'), story_id=data.get('story_id'))
    db.session.add(b)
    db.session.commit()
    return jsonify(obj_to_dict(b)), 201

@api_bp.route('/bugs/<int:bug_id>', methods=['GET'])
def get_bug(bug_id):
    b = Bug.query.get_or_404(bug_id)
    return jsonify(obj_to_dict(b))

@api_bp.route('/bugs/<int:bug_id>', methods=['PUT'])
def update_bug(bug_id):
    b = Bug.query.get_or_404(bug_id)
    data = request.get_json() or {}
    for k in ('title','description','status','severity','story_id'):
        if k in data:
            setattr(b, k, data[k])
    db.session.commit()
    return jsonify(obj_to_dict(b))

@api_bp.route('/bugs/<int:bug_id>', methods=['DELETE'])
def delete_bug(bug_id):
    b = Bug.query.get_or_404(bug_id)
    db.session.delete(b)
    db.session.commit()
    return '', 204

# Iterations
@api_bp.route('/iterations', methods=['GET'])
def list_iterations():
    its = Iteration.query.all()
    return jsonify([obj_to_dict(i) for i in its])

@api_bp.route('/iterations', methods=['POST'])
def create_iteration():
    data = request.get_json() or {}
    if 'name' not in data:
        abort(400, 'name required')
    it = Iteration(name=data['name'])
    db.session.add(it)
    db.session.commit()
    return jsonify(obj_to_dict(it)), 201

@api_bp.route('/releases', methods=['GET'])
def list_releases():
    rs = Release.query.all()
    return jsonify([obj_to_dict(r) for r in rs])

@api_bp.route('/releases', methods=['POST'])
def create_release():
    data = request.get_json() or {}
    if 'name' not in data:
        abort(400, 'name required')
    r = Release(name=data['name'])
    db.session.add(r)
    db.session.commit()
    return jsonify(obj_to_dict(r)), 201
