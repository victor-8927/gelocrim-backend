# Reescreve RotaScreen com teclado KM em grid e fluxo de 3 cliques
rota = r"""import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet,
  ActivityIndicator, Alert, Dimensions, ScrollView, TextInput
} from 'react-native';
import MapView, { Marker, Polyline, PROVIDER_GOOGLE } from 'react-native-maps';
import * as Location from 'expo-location';

const API_URL = 'https://antsy-gloomily-query.ngrok-free.dev/api/v1';
const DEPOSITO = { latitude: -3.093544, longitude: -60.075812 };
const { height } = Dimensions.get('window');

const CORES = {
  pending:   '#00BFFF',
  completed: '#00FF88',
  failed:    '#FF3355',
  reentrega: '#FFD700',
  adiada:    '#BF5FFF',
};

function decodePolyline(encoded) {
  const poly = []; let index = 0, lat = 0, lng = 0;
  while (index < encoded.length) {
    let shift = 0, result = 0, b;
    do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
    lat += (result & 1) ? ~(result >> 1) : (result >> 1); shift = 0; result = 0;
    do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
    lng += (result & 1) ? ~(result >> 1) : (result >> 1);
    poly.push({ latitude: lat / 1e5, longitude: lng / 1e5 });
  } return poly;
}

// Teclado numérico em grid 3x4
function TecladoKM({ valor, onChange }) {
  const keys = ['1','2','3','4','5','6','7','8','9','','0','⌫'];
  return (
    <View style={tkStyles.grid}>
      {keys.map((k, i) => (
        <TouchableOpacity key={i}
          style={[tkStyles.key, !k && tkStyles.keyVazio]}
          onPress={() => {
            if (!k) return;
            if (k === '⌫') onChange(valor.slice(0,-1));
            else onChange(valor + k);
          }}
          activeOpacity={k ? 0.7 : 1}
        >
          <Text style={tkStyles.keyTxt}>{k}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const tkStyles = StyleSheet.create({
  grid: { flexDirection:'row', flexWrap:'wrap', width:'100%', gap: 8, marginTop: 16 },
  key: { width: '30%', aspectRatio: 1.8, backgroundColor: 'rgba(0,191,255,0.12)',
    borderRadius: 12, alignItems:'center', justifyContent:'center',
    borderWidth: 1, borderColor: 'rgba(0,191,255,0.25)' },
  keyVazio: { backgroundColor: 'transparent', borderColor: 'transparent' },
  keyTxt: { color: '#fff', fontSize: 26, fontWeight: '700' },
});

export default function RotaScreen({ navigation, route }) {
  const { token } = route.params;
  const mapRef = useRef(null);
  const [stops, setStops]       = useState([]);
  const [rotaInfo, setRotaInfo] = useState(null);
  const [posicao, setPosicao]   = useState(null);
  const [loading, setLoading]   = useState(true);
  const [semRota, setSemRota]   = useState(false);
  const [stopSel, setStopSel]   = useState(null);
  const [modoLista, setModoLista] = useState(false);
  const [kmInicial, setKmInicial] = useState('');
  const [showKm, setShowKm]     = useState(false);
  const [kmConfirmado, setKmConfirmado] = useState(false);

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'ngrok-skip-browser-warning': '1'
  };

  useEffect(() => { iniciarGPS(); carregarRota(); }, []);

  async function iniciarGPS() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;
      const loc = await Location.getCurrentPositionAsync({});
      setPosicao({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });
    } catch {}
  }

  async function carregarRota() {
    setLoading(true); setSemRota(false);
    try {
      const datas = [];
      for (let i = 0; i < 3; i++) {
        const d = new Date(Date.now() - i * 86400000);
        datas.push(d.toISOString().slice(0, 10));
      }
      let rotaEncontrada = null;
      for (const data of datas) {
        const res = await fetch(`${API_URL}/routes?date=${data}`, { headers });
        if (!res.ok) continue;
        const rotas = await res.json();
        if (!Array.isArray(rotas)) continue;
        const validas = rotas.filter(r => r.status === 'released' || r.status === 'executing');
        if (validas.length > 0) { rotaEncontrada = validas[0]; break; }
      }
      if (!rotaEncontrada) { setSemRota(true); setLoading(false); return; }
      setRotaInfo(rotaEncontrada);
      if (rotaEncontrada.status === 'released') setShowKm(true);

      const resS = await fetch(`${API_URL}/routes/${rotaEncontrada.route_id}/stops`, { headers });
      const stopsData = await resS.json();
      if (Array.isArray(stopsData)) {
        const sorted = stopsData.sort((a, b) => (a.sequence||0) - (b.sequence||0));
        setStops(sorted);
        setTimeout(() => {
          if (mapRef.current) {
            const coords = [DEPOSITO, ...sorted.filter(s=>s.lat&&s.lng).map(s=>({
              latitude: parseFloat(s.lat), longitude: parseFloat(s.lng)
            }))];
            if (coords.length > 1) mapRef.current.fitToCoordinates(coords, {
              edgePadding: { top:100, right:40, bottom:280, left:40 }, animated:true
            });
          }
        }, 600);
      }
    } catch (e) { Alert.alert('Erro', String(e)); }
    finally { setLoading(false); }
  }

  async function confirmarKmEIniciar() {
    if (!kmInicial || kmInicial.length < 4) {
      Alert.alert('KM inválido', 'Informe pelo menos 4 dígitos.'); return;
    }
    try {
      await fetch(`${API_URL}/routes/${rotaInfo.route_id}/iniciar`, {
        method: 'POST', headers,
        body: JSON.stringify({ km_inicial: parseInt(kmInicial) })
      });
      setRotaInfo(p => ({ ...p, status: 'executing' }));
      setKmConfirmado(true);
      setShowKm(false);
    } catch (e) { Alert.alert('Erro', e.message); }
  }

  async function finalizarViagem() {
    Alert.alert('KM Final', 'Informe o KM final:', [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Finalizar', onPress: async () => {
        await fetch(`${API_URL}/routes/${rotaInfo.route_id}/finalizar`, { method: 'POST', headers });
        Alert.alert('🏁 Viagem Finalizada!', '', [
          { text: 'OK', onPress: () => navigation.replace('Login') }
        ]);
      }}
    ]);
  }

  function getCorStop(stop) {
    if (stop.status === 'completed') return CORES.completed;
    if (stop.status === 'failed')    return CORES.failed;
    if (stop.status === 'reentrega') return CORES.reentrega;
    if (stop.status === 'adiada')    return CORES.adiada;
    const prox = stops.find(s => s.status === 'pending');
    if (prox && prox.stop_id === stop.stop_id) return CORES.pending;
    return 'rgba(255,255,255,0.25)';
  }

  const completadas = stops.filter(s => s.status === 'completed').length;
  const total = stops.length;
  const pct = total > 0 ? Math.round(completadas / total * 100) : 0;

  if (loading) return (
    <View style={s.center}>
      <Text style={{ fontSize: 48 }}>❄</Text>
      <ActivityIndicator size="large" color="#00BFFF" style={{ marginTop: 16 }} />
      <Text style={s.dimTxt}>Carregando rota...</Text>
    </View>
  );

  if (semRota) return (
    <View style={s.center}>
      <Text style={{ fontSize: 48 }}>⏳</Text>
      <Text style={s.titulo}>Aguardando Liberação</Text>
      <Text style={s.sub}>Sua rota ainda não foi liberada.{'\n'}Aguarde o analista.</Text>
      <TouchableOpacity style={s.btnSec} onPress={carregarRota}>
        <Text style={s.btnSecTxt}>🔄 Verificar</Text>
      </TouchableOpacity>
    </View>
  );

  // Tela KM inicial
  if (showKm) return (
    <View style={[s.center, { justifyContent:'flex-start', paddingTop: 60 }]}>
      <Text style={{ fontSize: 40 }}>🚛</Text>
      <Text style={[s.titulo, { marginTop: 12 }]}>KM Inicial do Veículo</Text>
      <Text style={s.sub}>Obrigatório para iniciar a operação</Text>

      <View style={s.kmDisplay}>
        <Text style={s.kmValor}>{kmInicial || '_ _ _ _ _'}</Text>
        <Text style={s.kmUnidade}>km</Text>
      </View>

      <TecladoKM valor={kmInicial} onChange={setKmInicial} />

      <TouchableOpacity
        style={[s.btnPrimario, { marginTop: 24, opacity: kmInicial.length >= 4 ? 1 : 0.4 }]}
        onPress={confirmarKmEIniciar}
        disabled={kmInicial.length < 4}
      >
        <Text style={s.btnPrimarioTxt}>▶ INICIAR OPERAÇÃO</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={{ flex: 1 }}>
      <MapView ref={mapRef} style={StyleSheet.absoluteFillObject}
        provider={PROVIDER_GOOGLE}
        initialRegion={{ ...DEPOSITO, latitudeDelta: 0.08, longitudeDelta: 0.08 }}
      >
        <Marker coordinate={DEPOSITO} anchor={{ x:0.5, y:0.5 }}>
          <View style={s.depositoPin}><Text>🏭</Text></View>
        </Marker>
        {stops.map(stop => {
          const lat = parseFloat(stop.lat), lng = parseFloat(stop.lng);
          if (!lat || !lng) return null;
          const cor = getCorStop(stop);
          return (
            <Marker key={stop.stop_id} coordinate={{ latitude:lat, longitude:lng }}
              onPress={() => { setStopSel(stop); setModoLista(false); }}
              anchor={{ x:0.5, y:0.5 }}>
              <View style={[s.pin, { backgroundColor:cor, shadowColor:cor }]}>
                <Text style={s.pinNum}>{(stop.sequence||0)+1}</Text>
              </View>
            </Marker>
          );
        })}
        {posicao && (
          <Marker coordinate={posicao} anchor={{ x:0.5, y:0.5 }}>
            <View style={s.motOuter}><View style={s.motInner}/></View>
          </Marker>
        )}
      </MapView>

      {/* Header */}
      <View style={s.header}>
        <View>
          <Text style={s.headerBrand}>❄ {rotaInfo?.trip_number||'GELOCRIM'}</Text>
          <Text style={s.headerInfo}>{rotaInfo?.vehicle_plate} · {total} paradas · KM {kmInicial||'—'}</Text>
        </View>
        <View style={{ alignItems:'flex-end' }}>
          <Text style={s.headerPct}>{pct}%</Text>
          <Text style={s.headerSub}>{completadas}/{total}</Text>
        </View>
      </View>
      <View style={s.progressBar}>
        <View style={[s.progressFill, { width:`${pct}%` }]}/>
      </View>

      {/* Legenda */}
      <View style={s.legenda}>
        {[['#00FF88','Entregue'],['#FFD700','Reentrega'],['#FF3355','Falhou'],['#00BFFF','Próximo']].map(([cor,lb])=>(
          <View key={lb} style={{ flexDirection:'row', alignItems:'center', gap:4 }}>
            <View style={{ width:8, height:8, borderRadius:4, backgroundColor:cor }}/>
            <Text style={s.legendaTxt}>{lb}</Text>
          </View>
        ))}
      </View>

      {/* Botões flutuantes */}
      <View style={s.botoesFlut}>
        <TouchableOpacity style={s.btnFlut} onPress={()=>{setModoLista(!modoLista);setStopSel(null);}}>
          <Text style={{fontSize:18}}>📋</Text>
        </TouchableOpacity>
        {rotaInfo?.status==='executing' && (
          <TouchableOpacity style={[s.btnFlut,{borderColor:'#FF3355'}]} onPress={finalizarViagem}>
            <Text style={{fontSize:18}}>🏁</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Card stop */}
      {stopSel && !modoLista && (
        <View style={[s.card, { borderColor: getCorStop(stopSel) }]}>
          <View style={{flexDirection:'row', gap:10, marginBottom:8}}>
            <View style={[s.badge,{backgroundColor:getCorStop(stopSel)}]}>
              <Text style={s.badgeTxt}>{(stopSel.sequence||0)+1}</Text>
            </View>
            <View style={{flex:1}}>
              <Text style={s.cardLbl}>PARADA</Text>
              <Text style={s.cardNome} numberOfLines={1}>{stopSel.recipient_name}</Text>
              <Text style={s.cardCod}>COD: {stopSel.codparc||'—'}</Text>
              <Text style={s.cardEnd} numberOfLines={1}>{stopSel.address}</Text>
            </View>
            <TouchableOpacity onPress={()=>setStopSel(null)}>
              <Text style={{color:'#555',fontSize:20}}>✕</Text>
            </TouchableOpacity>
          </View>
          <View style={{flexDirection:'row',gap:10,marginBottom:12}}>
            <Text style={s.metaTxt}>🕐 {stopSel.eta||'--:--'}</Text>
            <Text style={s.metaTxt}>⚖️ {(stopSel.weight_kg||0).toFixed(0)}kg</Text>
          </View>
          <TouchableOpacity
            style={[s.btnEntrar, rotaInfo?.status!=='executing'&&{opacity:0.35}]}
            disabled={rotaInfo?.status!=='executing'}
            onPress={()=>navigation.navigate('Entrega',{
              stop:stopSel, token, routeId:rotaInfo?.route_id,
              proximoStop: stops.find(x=>x.sequence>(stopSel.sequence||0)&&x.status==='pending')
            })}
          >
            <Text style={s.btnEntrarTxt}>
              {rotaInfo?.status==='executing'?'📷 REGISTRAR ENTREGA →':'Inicie a operação primeiro'}
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Lista */}
      {modoLista && (
        <View style={s.lista}>
          <Text style={s.listaTitulo}>❄ SEQUÊNCIA DE ENTREGAS</Text>
          <ScrollView showsVerticalScrollIndicator={false}>
            {stops.map(stop=>(
              <TouchableOpacity key={stop.stop_id}
                style={[s.listaItem,{borderLeftColor:getCorStop(stop)}]}
                onPress={()=>{
                  setStopSel(stop); setModoLista(false);
                  mapRef.current?.animateToRegion({
                    latitude:parseFloat(stop.lat),longitude:parseFloat(stop.lng),
                    latitudeDelta:0.01,longitudeDelta:0.01
                  },500);
                }}>
                <View style={[s.badge,{backgroundColor:getCorStop(stop),width:26,height:26}]}>
                  <Text style={[s.badgeTxt,{fontSize:10}]}>{(stop.sequence||0)+1}</Text>
                </View>
                <View style={{flex:1}}>
                  <Text style={s.listaNome} numberOfLines={1}>{stop.recipient_name}</Text>
                  <Text style={s.listaSub}>COD:{stop.codparc||'—'} · {(stop.weight_kg||0).toFixed(0)}kg</Text>
                </View>
                <Text style={s.listaEta}>{stop.eta||'--:--'}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      )}
    </View>
  );
}

const s = StyleSheet.create({
  center:{flex:1,justifyContent:'center',alignItems:'center',backgroundColor:'#001020',padding:28},
  titulo:{color:'#fff',fontSize:22,fontWeight:'900',marginTop:12,textAlign:'center'},
  sub:{color:'rgba(255,255,255,0.45)',fontSize:13,marginTop:8,textAlign:'center',lineHeight:20},
  dimTxt:{color:'rgba(255,255,255,0.4)',marginTop:12,fontSize:13},
  btnSec:{marginTop:24,backgroundColor:'rgba(0,191,255,0.12)',borderRadius:12,padding:14,paddingHorizontal:28,borderWidth:1,borderColor:'rgba(0,191,255,0.3)'},
  btnSecTxt:{color:'#00BFFF',fontWeight:'700',fontSize:14},
  btnPrimario:{backgroundColor:'#00BFFF',borderRadius:14,padding:16,paddingHorizontal:32,alignItems:'center',width:'90%'},
  btnPrimarioTxt:{color:'#001020',fontWeight:'900',fontSize:15,letterSpacing:2},
  kmDisplay:{marginTop:24,backgroundColor:'rgba(0,191,255,0.08)',borderRadius:16,paddingHorizontal:32,paddingVertical:20,borderWidth:1,borderColor:'rgba(0,191,255,0.3)',flexDirection:'row',alignItems:'baseline',gap:8,width:'90%',justifyContent:'center'},
  kmValor:{color:'#00BFFF',fontSize:42,fontWeight:'900',letterSpacing:6},
  kmUnidade:{color:'rgba(0,191,255,0.5)',fontSize:16,fontWeight:'600'},
  header:{position:'absolute',top:0,left:0,right:0,backgroundColor:'rgba(0,8,25,0.96)',flexDirection:'row',justifyContent:'space-between',alignItems:'center',padding:14,paddingTop:44},
  headerBrand:{color:'#00BFFF',fontSize:11,fontWeight:'800',letterSpacing:4,marginBottom:2},
  headerInfo:{color:'#fff',fontSize:13,fontWeight:'700'},
  headerPct:{color:'#00FF88',fontSize:22,fontWeight:'900'},
  headerSub:{color:'rgba(255,255,255,0.35)',fontSize:10},
  progressBar:{position:'absolute',top:88,left:0,right:0,height:3,backgroundColor:'rgba(255,255,255,0.08)'},
  progressFill:{height:3,backgroundColor:'#00FF88'},
  legenda:{position:'absolute',top:92,left:0,right:0,flexDirection:'row',justifyContent:'center',gap:14,padding:5,backgroundColor:'rgba(0,8,25,0.75)'},
  legendaTxt:{color:'rgba(255,255,255,0.6)',fontSize:9,fontWeight:'600'},
  botoesFlut:{position:'absolute',right:14,top:120,gap:10},
  btnFlut:{width:46,height:46,borderRadius:23,backgroundColor:'rgba(0,8,25,0.92)',alignItems:'center',justifyContent:'center',elevation:5,borderWidth:1,borderColor:'rgba(0,191,255,0.25)'},
  pin:{width:30,height:30,borderRadius:15,alignItems:'center',justifyContent:'center',borderWidth:2,borderColor:'#001020',elevation:8,shadowOpacity:0.9,shadowRadius:8},
  pinNum:{color:'#001020',fontWeight:'900',fontSize:11},
  depositoPin:{width:36,height:36,borderRadius:18,backgroundColor:'rgba(0,8,25,0.95)',alignItems:'center',justifyContent:'center',borderWidth:2,borderColor:'#00BFFF'},
  motOuter:{width:20,height:20,borderRadius:10,backgroundColor:'rgba(0,191,255,0.2)',alignItems:'center',justifyContent:'center'},
  motInner:{width:12,height:12,borderRadius:6,backgroundColor:'#00BFFF',borderWidth:2,borderColor:'#fff'},
  card:{position:'absolute',bottom:20,left:14,right:14,backgroundColor:'rgba(0,8,25,0.97)',borderRadius:18,padding:16,elevation:12,borderWidth:1},
  cardLbl:{color:'#00BFFF',fontSize:9,fontWeight:'800',letterSpacing:3,marginBottom:2},
  cardNome:{fontSize:15,fontWeight:'800',color:'#fff'},
  cardCod:{fontSize:10,color:'#00BFFF',marginTop:1},
  cardEnd:{fontSize:11,color:'rgba(255,255,255,0.4)',marginTop:2},
  badge:{width:32,height:32,borderRadius:16,alignItems:'center',justifyContent:'center'},
  badgeTxt:{color:'#001020',fontWeight:'900',fontSize:13},
  metaTxt:{fontSize:12,color:'rgba(255,255,255,0.55)'},
  btnEntrar:{backgroundColor:'#00BFFF',borderRadius:12,padding:13,alignItems:'center'},
  btnEntrarTxt:{color:'#001020',fontWeight:'900',fontSize:13,letterSpacing:1},
  lista:{position:'absolute',bottom:0,left:0,right:0,backgroundColor:'rgba(0,8,25,0.98)',borderTopLeftRadius:20,borderTopRightRadius:20,maxHeight:height*0.6,padding:18,elevation:12},
  listaTitulo:{fontSize:10,fontWeight:'800',color:'#00BFFF',marginBottom:12,letterSpacing:3},
  listaItem:{flexDirection:'row',alignItems:'center',gap:10,paddingVertical:11,borderBottomWidth:1,borderBottomColor:'rgba(255,255,255,0.05)',borderLeftWidth:3,paddingLeft:10},
  listaNome:{fontSize:13,fontWeight:'700',color:'#fff'},
  listaSub:{fontSize:10,color:'rgba(0,191,255,0.6)',marginTop:1},
  listaEta:{fontSize:12,color:'#00BFFF',fontWeight:'700'},
});
"""

with open(r'C:\gelocrim-motorista\screens\RotaScreen.js', 'w', encoding='utf-8') as f:
    f.write(rota)
print('RotaScreen.js atualizado!')
